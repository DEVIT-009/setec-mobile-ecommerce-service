import uuid
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from domain.category.entity.category import Category as DomainCategory
from domain.product.entity.product import Product as DomainProduct, ProductVariant as DomainProductVariant
from domain.cart.entity.cart import Cart as DomainCart, CartItem as DomainCartItem
from domain.order.entity.order import Order as DomainOrder
from domain.user.entity.user import User as DomainUser
from domain.address.entity.address import Address as DomainAddress

from infrastructure.persistence.models.ecom_user_model import EcomUser, UserAddress
from infrastructure.persistence.models.store_model import Store
from infrastructure.persistence.models.category_model import Category
from infrastructure.persistence.models.product_model import Product, ProductImage, ProductVariant
from infrastructure.persistence.models.cart_model import Cart, CartItem
from infrastructure.persistence.models.order_model import Order, OrderItem, OrderStatusHistory
from infrastructure.persistence.models.payment_model import PaymentBatch
from infrastructure.persistence.models.shipment_model import Shipment, ShipmentEvent
from domain.order.exception.order_exception import OrderException
from domain.shipment.exception.shipment_exception import ShipmentException
from domain.review.exception.review_exception import ReviewException
from domain.address.exception.address_exception import AddressException
from shared.security.jwt_util import JwtUtil

from application.category.factory.category_service_factory import category_service_factory
from application.product.factory.product_service_factory import product_service_factory
from application.cart.factory.cart_service_factory import cart_service_factory
from application.order.factory.order_service_factory import order_service_factory
from application.payment.factory.payment_service_factory import payment_service_factory
from application.shipment.factory.shipment_service_factory import shipment_service_factory
from application.user.factory.user_service_factory import user_service_factory
from application.address.factory.address_service_factory import address_service_factory
from application.store.factory.store_service_factory import store_service_factory
from application.notification.factory.notification_service_factory import notification_service_factory
from application.conversation.factory.conversation_service_factory import conversation_service_factory
from application.review.factory.review_service_factory import review_service_factory


class HexagonalArchitectureTestSuite(TestCase):

    def setUp(self):
        self.user = EcomUser.objects.create(
            email="customer@example.com",
            password_hash=make_password("Password123!"),
            first_name="John",
            last_name="Doe",
            status="active",
        )
        self.seller = EcomUser.objects.create(
            email="seller@example.com",
            first_name="Jane",
            last_name="StoreOwner",
            status="active",
        )
        self.store = Store.objects.create(
            owner=self.seller,
            name="Tech Gadgets",
            slug="tech-gadgets",
            status="active",
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            status="active",
        )
        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Wireless Headphones",
            slug="wireless-headphones",
            base_price=Decimal("99.99"),
            status="active",
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            image_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
            is_primary=True,
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            name="Black",
            price=Decimal("99.99"),
            stock_quantity=50,
            status="active",
        )
        self.address = UserAddress.objects.create(
            user=self.user,
            recipient_name="John Doe",
            phone_number="1234567890",
            address_line_1="123 Main St",
            city="Metropolis",
            country_code="US",
            is_default=True,
        )

    def test_user_and_address_facades(self):
        user_service = user_service_factory()
        user_data = user_service.get_me(str(self.user.id))
        self.assertEqual(user_data["email"], "customer@example.com")
        self.assertIsNotNone(user_data["default_address"])

        address_service = address_service_factory()
        addresses = address_service.list(str(self.user.id))
        self.assertEqual(len(addresses), 1)
        self.assertEqual(addresses[0]["recipient_name"], "John Doe")

    def test_product_and_store_facades(self):
        product_service = product_service_factory()
        products = product_service.list_active({}, page=1, page_size=10, user_id=str(self.user.id))
        self.assertEqual(products["total"], 1)
        self.assertEqual(products["items"][0]["name"], "Wireless Headphones")

        detail = product_service.get_by_id(str(self.product.id), user_id=str(self.user.id))
        self.assertEqual(detail["name"], "Wireless Headphones")
        self.assertEqual(len(detail["images"]), 1)
        self.assertEqual(len(detail["variants"]), 1)

        store_service = store_service_factory()
        store_data = store_service.get_by_slug("tech-gadgets")
        self.assertEqual(store_data["name"], "Tech Gadgets")

    def test_cart_and_order_checkout_flow(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 2,
        })
        self.assertEqual(len(cart_data["items"]), 1)
        self.assertEqual(cart_data["totals"]["selected_item_count"], 2)
        self.assertEqual(Decimal(cart_data["totals"]["total_amount"]), Decimal("199.98"))

        order_service = order_service_factory()
        orders = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-IDEMP-KEY-12345",
        )
        self.assertEqual(len(orders), 1)
        placed_order = orders[0]
        self.assertEqual(placed_order["status"], "pending")
        self.assertEqual(Decimal(placed_order["total_amount"]), Decimal("199.98"))
        self.assertEqual(len(placed_order["items"]), 1)
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 48)

        # Cart should now be empty of active items
        refreshed_cart = cart_service.get_or_create_cart(str(self.user.id))
        self.assertEqual(len(refreshed_cart["items"]), 0)

        order_service.cancel(placed_order["id"], str(self.user.id))
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)

    def test_checkout_rejects_insufficient_variant_stock(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 51,
        })

        order_service = order_service_factory()
        with self.assertRaises(OrderException) as context:
            order_service.place_orders(
                user_id=str(self.user.id),
                cart_id=cart_data["id"],
                shipping_address_id=str(self.address.id),
                idempotency_key="TEST-INSUFFICIENT-STOCK",
            )

        self.assertEqual(context.exception.error_code, "INSUFFICIENT_STOCK")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)

    def test_admin_cancellation_restores_variant_stock_once(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 3,
        })

        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-ADMIN-CANCEL-STOCK",
        )[0]

        order_service.update_status(
            placed_order["id"],
            "cancelled",
            changed_by_user_id=str(self.seller.id),
            note="Cancelled by admin",
        )
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)

        order_service.update_status(
            placed_order["id"],
            "cancelled",
            changed_by_user_id=str(self.seller.id),
            note="Repeated cancellation",
        )
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="cancelled",
            ).count(),
            1,
        )

    def test_admin_failure_refunds_payment_and_restores_stock_once(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 2,
        })
        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-ADMIN-FAILED-ORDER",
        )[0]
        payment_service = payment_service_factory()
        payment_service.complete(
            order_id=placed_order["id"],
            user_id=str(self.user.id),
            idempotency_key="TEST-ADMIN-FAILED-PAYMENT",
        )

        failed_order = order_service.mark_failed(
            order_id=placed_order["id"],
            changed_by_user_id=str(self.seller.id),
            note="Fulfillment could not be completed",
        )
        repeated_order = order_service.mark_failed(
            order_id=placed_order["id"],
            changed_by_user_id=str(self.seller.id),
            note="Repeated request",
        )

        self.assertEqual(failed_order["status"], "failed")
        self.assertEqual(repeated_order["status"], "failed")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)
        self.assertEqual(
            payment_service.get_for_order(placed_order["id"], str(self.user.id))["status"],
            "refunded",
        )
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="failed",
            ).count(),
            1,
        )
        with self.assertRaises(OrderException) as context:
            order_service.update_status(
                placed_order["id"],
                "confirmed",
                changed_by_user_id=str(self.seller.id),
                note="Invalid reopen attempt",
            )
        self.assertEqual(context.exception.error_code, "ORDER_INVALID_STATUS_TRANSITION")

    def test_internal_payment_confirms_order_and_is_idempotent(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 2,
        })
        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-ORDER-FOR-PAYMENT",
        )[0]

        payment_service = payment_service_factory()
        payment = payment_service.complete(
            order_id=placed_order["id"],
            user_id=str(self.user.id),
            idempotency_key="TEST-PAYMENT-IDEMPOTENCY",
        )
        repeated_payment = payment_service.complete(
            order_id=placed_order["id"],
            user_id=str(self.user.id),
            idempotency_key="TEST-PAYMENT-IDEMPOTENCY",
        )

        self.assertEqual(payment["status"], "succeeded")
        self.assertEqual(payment["amount"], "199.98")
        self.assertEqual(repeated_payment["id"], payment["id"])

        confirmed_order = order_service.get_detail(placed_order["id"], str(self.user.id))
        self.assertEqual(confirmed_order["status"], "confirmed")
        self.assertEqual(confirmed_order["payment"]["id"], payment["id"])

        order_service.cancel(placed_order["id"], str(self.user.id))
        refunded_payment = payment_service.get_for_order(placed_order["id"], str(self.user.id))
        self.assertEqual(refunded_payment["status"], "refunded")
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)

    def test_internal_batch_payment_confirms_multiple_store_orders(self):
        second_store = Store.objects.create(
            owner=self.seller,
            name="Home Goods",
            slug="home-goods",
            status="active",
        )
        second_product = Product.objects.create(
            store=second_store,
            category=self.category,
            name="Desk Lamp",
            slug="desk-lamp",
            base_price=Decimal("25.00"),
            status="active",
        )
        second_variant = ProductVariant.objects.create(
            product=second_product,
            name="White",
            price=Decimal("25.00"),
            stock_quantity=10,
            status="active",
        )

        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 1,
        })
        cart_service.add_item(str(self.user.id), {
            "product_id": str(second_product.id),
            "product_variant_id": str(second_variant.id),
            "quantity": 2,
        })

        order_service = order_service_factory()
        orders = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-MULTI-STORE-ORDER",
        )
        order_ids = [order["id"] for order in orders]
        self.assertEqual(len(order_ids), 2)

        payment_service = payment_service_factory()
        batch = payment_service.complete_batch(
            order_ids=order_ids,
            user_id=str(self.user.id),
            idempotency_key="TEST-BATCH-PAYMENT",
        )
        repeated_batch = payment_service.complete_batch(
            order_ids=list(reversed(order_ids)),
            user_id=str(self.user.id),
            idempotency_key="TEST-BATCH-PAYMENT",
        )

        self.assertEqual(batch["status"], "succeeded")
        self.assertEqual(batch["total_amount"], "149.99")
        self.assertEqual(set(batch["order_ids"]), set(order_ids))
        self.assertEqual(len(batch["payments"]), 2)
        self.assertEqual(repeated_batch["id"], batch["id"])
        for order_id in order_ids:
            self.assertEqual(
                order_service.get_detail(order_id, str(self.user.id))["status"],
                "confirmed",
            )

        order_service.cancel(order_ids[0], str(self.user.id))
        batch_model = PaymentBatch.objects.get(id=batch["id"])
        self.assertEqual(batch_model.status, "partially_refunded")

        order_service.cancel(order_ids[1], str(self.user.id))
        batch_model.refresh_from_db()
        self.assertEqual(batch_model.status, "refunded")

    def test_internal_batch_payment_failure_restores_stock_and_is_idempotent(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 4,
        })
        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-FAILED-PAYMENT-ORDER",
        )[0]
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 46)

        payment_service = payment_service_factory()
        batch = payment_service.complete_batch(
            order_ids=[placed_order["id"]],
            user_id=str(self.user.id),
            idempotency_key="TEST-FAILED-BATCH-PAYMENT",
            outcome="failed",
            failure_reason="Mock card declined",
        )
        repeated_batch = payment_service.complete_batch(
            order_ids=[placed_order["id"]],
            user_id=str(self.user.id),
            idempotency_key="TEST-FAILED-BATCH-PAYMENT",
            outcome="succeeded",
        )

        self.assertEqual(batch["status"], "failed")
        self.assertEqual(batch["failure_reason"], "Mock card declined")
        self.assertEqual(batch["payments"][0]["status"], "failed")
        self.assertEqual(repeated_batch["id"], batch["id"])
        self.assertEqual(repeated_batch["status"], "failed")
        self.assertEqual(
            order_service.get_detail(placed_order["id"], str(self.user.id))["status"],
            "failed",
        )
        self.variant.refresh_from_db()
        self.assertEqual(self.variant.stock_quantity, 50)
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="failed",
            ).count(),
            1,
        )

    def test_admin_marks_confirmed_order_processing_once(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 1,
        })
        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-PROCESSING-ORDER",
        )[0]
        payment_service_factory().complete_batch(
            order_ids=[placed_order["id"]],
            user_id=str(self.user.id),
            idempotency_key="TEST-PROCESSING-PAYMENT",
        )

        processing_order = order_service.mark_processing(
            order_id=placed_order["id"],
            changed_by_user_id=str(self.seller.id),
            note="Store started preparing the products",
        )
        repeated_order = order_service.mark_processing(
            order_id=placed_order["id"],
            changed_by_user_id=str(self.seller.id),
            note="Repeated request",
        )

        self.assertEqual(processing_order["status"], "processing")
        self.assertEqual(repeated_order["status"], "processing")
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="processing",
            ).count(),
            1,
        )

    def test_shipment_create_pack_and_handoff_flow(self):
        cart_service = cart_service_factory()
        cart_data = cart_service.add_item(str(self.user.id), {
            "product_id": str(self.product.id),
            "product_variant_id": str(self.variant.id),
            "quantity": 1,
        })
        order_service = order_service_factory()
        placed_order = order_service.place_orders(
            user_id=str(self.user.id),
            cart_id=cart_data["id"],
            shipping_address_id=str(self.address.id),
            idempotency_key="TEST-SHIPMENT-ORDER",
        )[0]
        payment_service_factory().complete_batch(
            order_ids=[placed_order["id"]],
            user_id=str(self.user.id),
            idempotency_key="TEST-SHIPMENT-PAYMENT",
        )
        order_service.mark_processing(
            order_id=placed_order["id"],
            changed_by_user_id=str(self.seller.id),
            note="Preparing order",
        )

        shipment_service = shipment_service_factory()
        shipment = shipment_service.create_for_order(
            order_id=placed_order["id"],
            actor_id=str(self.seller.id),
            note="Shipment created",
        )
        repeated_shipment = shipment_service.create_for_order(
            order_id=placed_order["id"],
            actor_id=str(self.seller.id),
            note="Repeated creation",
        )
        self.assertEqual(shipment["status"], "pending")
        self.assertEqual(repeated_shipment["id"], shipment["id"])

        packed = shipment_service.mark_packed(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            note="Products packed",
        )
        repeated_packed = shipment_service.mark_packed(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            note="Repeated packing",
        )
        self.assertEqual(packed["status"], "packed")
        self.assertEqual(repeated_packed["status"], "packed")

        handed_off = shipment_service.handoff(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            data={
                "carrier_name": "DHL Express",
                "tracking_number": "DHL-123456",
                "location": "Phnom Penh warehouse",
                "note": "Package handed to carrier",
            },
        )
        repeated_handoff = shipment_service.handoff(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            data={
                "carrier_name": "DHL Express",
                "tracking_number": "DHL-123456",
            },
        )
        self.assertEqual(handed_off["status"], "in_transit")
        self.assertEqual(handed_off["carrier_name"], "DHL Express")
        self.assertEqual(repeated_handoff["status"], "in_transit")
        self.assertEqual(
            order_service.get_detail(placed_order["id"], str(self.user.id))["status"],
            "shipped",
        )
        self.assertEqual(Shipment.objects.filter(order_id=placed_order["id"]).count(), 1)
        self.assertEqual(ShipmentEvent.objects.filter(shipment_id=shipment["id"]).count(), 3)
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="shipped",
            ).count(),
            1,
        )

        checkpoint = shipment_service.record_checkpoint(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            data={
                "location": "Phnom Penh sorting center",
                "description": "Package scanned at sorting center",
            },
        )
        self.assertEqual(checkpoint["status"], "in_transit")

        out_for_delivery = shipment_service.mark_out_for_delivery(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            data={
                "location": "Phnom Penh delivery hub",
                "note": "Courier is delivering the package",
            },
        )
        repeated_out_for_delivery = shipment_service.mark_out_for_delivery(
            shipment_id=shipment["id"],
            actor_id=str(self.seller.id),
            data={},
        )
        self.assertEqual(out_for_delivery["status"], "out_for_delivery")
        self.assertEqual(repeated_out_for_delivery["status"], "out_for_delivery")

        other_customer = EcomUser.objects.create(
            email="other-customer@example.com",
            status="active",
        )
        with self.assertRaises(ShipmentException):
            shipment_service.confirm_delivery(
                shipment_id=shipment["id"],
                user_id=str(other_customer.id),
                note="Not my shipment",
            )

        delivered = shipment_service.confirm_delivery(
            shipment_id=shipment["id"],
            user_id=str(self.user.id),
            note="Product received in good condition",
        )
        repeated_delivery = shipment_service.confirm_delivery(
            shipment_id=shipment["id"],
            user_id=str(self.user.id),
            note="Repeated confirmation",
        )
        self.assertEqual(delivered["status"], "delivered")
        self.assertIsNotNone(delivered["delivered_at"])
        self.assertEqual(repeated_delivery["status"], "delivered")
        self.assertEqual(
            order_service.get_detail(placed_order["id"], str(self.user.id))["status"],
            "delivered",
        )
        self.assertEqual(ShipmentEvent.objects.filter(shipment_id=shipment["id"]).count(), 6)
        self.assertEqual(
            OrderStatusHistory.objects.filter(
                order_id=placed_order["id"],
                to_status="delivered",
            ).count(),
            1,
        )

    def test_notification_and_conversation_facades(self):
        notif_service = notification_service_factory()
        notif_service.create_admin_notification({
            "user_id": str(self.user.id),
            "type": "order",
            "title": "Order Placed",
            "body": "Your order was placed successfully",
        })
        unread = notif_service.unread_count(str(self.user.id))
        self.assertEqual(unread["unread_count"], 1)

        conv_service = conversation_service_factory()
        conv = conv_service.create_conversation(str(self.user.id), {
            "store_id": str(self.store.id),
            "initial_message": "Hello, I have a question about my order",
        })
        self.assertEqual(conv["customer_id"], str(self.user.id))
        messages = conv_service.list_messages(str(self.user.id), conv["id"])
        self.assertEqual(messages["total"], 1)

    def test_auth_login_endpoint(self):
        # Test POST /api/v1/auth/login (without trailing slash)
        resp_no_slash = self.client.post(
            "/api/v1/auth/login",
            data={"email": "customer@example.com", "password": "Password123!"},
            content_type="application/json",
        )
        self.assertEqual(resp_no_slash.status_code, 200)
        self.assertIn("access_token", resp_no_slash.json()["data"])

        # Test POST /api/v1/auth/login/ (with trailing slash)
        resp_slash = self.client.post(
            "/api/v1/auth/login/",
            data={"email": "customer@example.com", "password": "Password123!"},
            content_type="application/json",
        )
        self.assertEqual(resp_slash.status_code, 200)
        self.assertIn("access_token", resp_slash.json()["data"])

    def test_review_validations(self):
        review_service = review_service_factory()

        # 1. Non-existent product_id raises 404 PRODUCT_NOT_FOUND
        fake_product_id = str(uuid.uuid4())
        with self.assertRaises(ReviewException) as ctx:
            review_service.create(str(self.user.id), {
                "product_id": fake_product_id,
                "rating": 5,
                "title": "Great",
                "body": "Loved it",
            })
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.error_code, "PRODUCT_NOT_FOUND")

        # 2. Non-existent order_item_id raises 404 ORDER_ITEM_NOT_FOUND
        fake_order_item_id = str(uuid.uuid4())
        with self.assertRaises(ReviewException) as ctx:
            review_service.create(str(self.user.id), {
                "product_id": str(self.product.id),
                "order_item_id": fake_order_item_id,
                "rating": 5,
                "title": "Great",
                "body": "Loved it",
            })
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.error_code, "ORDER_ITEM_NOT_FOUND")

        # 3. order_item belonging to a different user raises 400 INVALID_ORDER_ITEM
        other_order = Order.objects.create(
            order_number="ORD-TEST-9999",
            user=self.seller,
            store=self.store,
            status="delivered",
            total_amount=Decimal("99.99"),
        )
        other_item = OrderItem.objects.create(
            order=other_order,
            product=self.product,
            product_name_snapshot="Wireless Headphones",
            unit_price=Decimal("99.99"),
            quantity=1,
            line_total=Decimal("99.99"),
        )
        with self.assertRaises(ReviewException) as ctx:
            review_service.create(str(self.user.id), {
                "product_id": str(self.product.id),
                "order_item_id": str(other_item.id),
                "rating": 5,
                "title": "Great",
                "body": "Loved it",
            })
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.error_code, "INVALID_ORDER_ITEM")

        # 4. order_item belonging to a different product raises 400 INVALID_ORDER_ITEM
        other_product = Product.objects.create(
            store=self.store,
            name="USB-C Cable",
            slug="usbc-cable",
            base_price=Decimal("19.99"),
            status="active",
        )
        user_order = Order.objects.create(
            order_number="ORD-TEST-1111",
            user=self.user,
            store=self.store,
            status="delivered",
            total_amount=Decimal("19.99"),
        )
        user_other_item = OrderItem.objects.create(
            order=user_order,
            product=other_product,
            product_name_snapshot="USB-C Cable",
            unit_price=Decimal("19.99"),
            quantity=1,
            line_total=Decimal("19.99"),
        )
        with self.assertRaises(ReviewException) as ctx:
            review_service.create(str(self.user.id), {
                "product_id": str(self.product.id),
                "order_item_id": str(user_other_item.id),
                "rating": 5,
                "title": "Great",
                "body": "Loved it",
            })
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.error_code, "INVALID_ORDER_ITEM")

        # 5. Successful review without order_item_id
        valid_review = review_service.create(str(self.user.id), {
            "product_id": str(self.product.id),
            "rating": 5,
            "title": "Legit Product",
            "body": "Highly recommended!",
        })
        self.assertEqual(valid_review["rating"], 5)
        self.assertEqual(valid_review["title"], "Legit Product")

        # 6. Successful review with valid matching order_item_id
        user_item = OrderItem.objects.create(
            order=user_order,
            product=self.product,
            product_name_snapshot="Wireless Headphones",
            unit_price=Decimal("99.99"),
            quantity=1,
            line_total=Decimal("99.99"),
        )
        valid_order_review = review_service.create(str(self.user.id), {
            "product_id": str(self.product.id),
            "order_item_id": str(user_item.id),
            "rating": 4,
            "title": "Verified Purchase Review",
            "body": "Arrived on time!",
        })
        self.assertEqual(valid_order_review["order_item_id"], str(user_item.id))

        # 7. Duplicate review for same order_item_id raises 400 REVIEW_DUPLICATE
        with self.assertRaises(ReviewException) as ctx:
            review_service.create(str(self.user.id), {
                "product_id": str(self.product.id),
                "order_item_id": str(user_item.id),
                "rating": 5,
                "title": "Another review",
                "body": "Should fail",
            })
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.error_code, "REVIEW_DUPLICATE")

        # 8. Test via API endpoint POST /api/v1/products/<product_id>/reviews/ with fake order_item_id
        login_resp = self.client.post(
            "/api/v1/auth/login/",
            data={"email": "customer@example.com", "password": "Password123!"},
            content_type="application/json",
        )
        token = login_resp.json()["data"]["access_token"]
        api_resp = self.client.post(
            f"/api/v1/products/{self.product.id}/reviews/",
            data={
                "rating": 5,
                "title": "API Review",
                "order_item_id": str(uuid.uuid4()),
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(api_resp.status_code, 404)
        self.assertEqual(api_resp.json()["error"]["code"], "ORDER_ITEM_NOT_FOUND")

        # 9. Test public GET /api/v1/reviews/ and GET /api/v1/reviews/<review_id>/
        list_resp = self.client.get("/api/v1/reviews/")
        self.assertEqual(list_resp.status_code, 200)
        self.assertTrue(len(list_resp.json()["data"]) >= 1)

        filter_resp = self.client.get(f"/api/v1/reviews/?product_id={self.product.id}")
        self.assertEqual(filter_resp.status_code, 200)
        self.assertTrue(len(filter_resp.json()["data"]) >= 1)

        review_id = list_resp.json()["data"][0]["id"]
        detail_resp = self.client.get(f"/api/v1/reviews/{review_id}/")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertEqual(detail_resp.json()["data"]["id"], review_id)

        # 10. Test public alias /api/v1/public/reviews/
        pub_resp = self.client.get("/api/v1/public/reviews/")
        self.assertEqual(pub_resp.status_code, 200)

    def test_category_facade_and_routes(self):
        cat_service = category_service_factory()

        # 1. Create root category
        cat = cat_service.create({
            "name": "Audio",
            "slug": "audio",
            "status": "active",
        })
        self.assertEqual(cat["slug"], "audio")
        root_id = cat["id"]

        # 2. Create child category
        child = cat_service.create({
            "name": "Headphones",
            "slug": "audio-headphones",
            "parent_id": root_id,
            "status": "active",
        })
        self.assertEqual(child["parent_id"], root_id)

        # 3. Test get_tree
        tree = cat_service.get_tree()
        audio_node = next((n for n in tree if n["id"] == root_id), None)
        self.assertIsNotNone(audio_node)
        self.assertEqual(len(audio_node["children"]), 1)
        self.assertEqual(audio_node["children"][0]["slug"], "audio-headphones")

        # 4. Test get_by_id and get_by_slug
        by_id = cat_service.get_by_id(root_id)
        self.assertEqual(by_id["name"], "Audio")
        by_slug = cat_service.get_by_slug("audio")
        self.assertEqual(by_slug["id"], root_id)

        # 5. Test update by id
        updated = cat_service.update(root_id, {"name": "Audio & Sound", "slug": "audio-sound"}, partial=True)
        self.assertEqual(updated["name"], "Audio & Sound")
        self.assertEqual(updated["slug"], "audio-sound")

        # 6. Test soft delete by id
        cat_service.soft_delete(root_id)

        # 7. Test public routes
        resp_list = self.client.get("/api/v1/public/categories/")
        self.assertEqual(resp_list.status_code, 200)

        resp_compat_list = self.client.get("/api/v1/categories/")
        self.assertEqual(resp_compat_list.status_code, 200)

        resp_tree = self.client.get("/api/v1/public/categories/tree/")
        self.assertEqual(resp_tree.status_code, 200)

        resp_compat_tree = self.client.get("/api/v1/categories/tree/")
        self.assertEqual(resp_compat_tree.status_code, 200)

    def test_address_facade_comprehensive(self):
        address_service = address_service_factory()
        user_id = str(self.user.id)

        # 1. Invalid country code validation
        with self.assertRaises(AddressException):
            address_service.create(user_id, {
                "recipient_name": "Alice",
                "phone_number": "1234567890",
                "address_line_1": "456 Market St",
                "city": "Metropolis",
                "country_code": "USA",
            })

        # 2. Create address with is_default=True
        addr1 = address_service.create(user_id, {
            "label": "Work",
            "recipient_name": "Alice Smith",
            "phone_number": "0987654321",
            "address_line_1": "456 Market St",
            "city": "Metropolis",
            "country_code": "US",
            "is_default": True,
        }, actor_id=user_id)
        self.assertEqual(addr1["label"], "Work")
        self.assertTrue(addr1["is_default"])

        # Prior default address (self.address) should now have is_default=False
        prior_default = address_service.get(str(self.address.id), user_id)
        self.assertFalse(prior_default["is_default"])

        # 3. Retrieve address
        retrieved = address_service.get(addr1["id"], user_id)
        self.assertEqual(retrieved["id"], addr1["id"])
        self.assertEqual(retrieved["recipient_name"], "Alice Smith")

        # 4. Scoping: other user cannot access addr1
        other_user_id = str(self.seller.id)
        with self.assertRaises(AddressException):
            address_service.get(addr1["id"], other_user_id)

        # 5. Partial update
        updated = address_service.update(addr1["id"], user_id, {
            "recipient_name": "Alice Wonderland",
        }, partial=True, actor_id=user_id)
        self.assertEqual(updated["recipient_name"], "Alice Wonderland")
        self.assertEqual(updated["address_line_1"], "456 Market St")

        # 6. Set default
        address_service.set_default(str(self.address.id), user_id, actor_id=user_id)
        refreshed_addr = address_service.get(str(self.address.id), user_id)
        self.assertTrue(refreshed_addr["is_default"])
        refreshed_addr1 = address_service.get(addr1["id"], user_id)
        self.assertFalse(refreshed_addr1["is_default"])

        # 7. Soft delete
        address_service.delete(addr1["id"], user_id, actor_id=user_id)
        with self.assertRaises(AddressException):
            address_service.get(addr1["id"], user_id)

        # List should now exclude deleted
        active_list = address_service.list(user_id)
        self.assertEqual(len(active_list), 1)
        self.assertEqual(active_list[0]["id"], str(self.address.id))

    def test_address_api_endpoints_and_auth(self):
        token = JwtUtil.generate_token_for_ecom(self.user, roles=["customer"])
        auth_header = f"Bearer {token}"

        # 1. Unauthenticated request -> 401
        resp = self.client.get("/api/v1/customer/addresses/")
        self.assertEqual(resp.status_code, 401)

        # 2. List addresses -> 200
        resp = self.client.get(
            "/api/v1/customer/addresses/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["data"]), 1)

        # 3. Create address -> 201
        create_payload = {
            "label": "Home Office",
            "recipient_name": "Jane Doe",
            "phone_number": "5551234567",
            "address_line_1": "789 Pine Ave",
            "city": "Capital City",
            "country_code": "US",
            "is_default": False,
        }
        resp = self.client.post(
            "/api/v1/customer/addresses/",
            data=create_payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 201)
        new_id = resp.json()["data"]["id"]
        self.assertEqual(resp.json()["data"]["recipient_name"], "Jane Doe")

        # 4. Retrieve address by ID -> 200
        resp = self.client.get(
            f"/api/v1/customer/addresses/{new_id}/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["label"], "Home Office")

        # 5. Full update (PUT) -> 200
        update_payload = {
            "label": "HQ",
            "recipient_name": "Jane Doe HQ",
            "phone_number": "5559876543",
            "address_line_1": "100 Corporate Blvd",
            "city": "Capital City",
            "country_code": "US",
            "is_default": False,
        }
        resp = self.client.put(
            f"/api/v1/customer/addresses/{new_id}/",
            data=update_payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["label"], "HQ")
        self.assertEqual(resp.json()["data"]["recipient_name"], "Jane Doe HQ")

        # 6. Partial update (PATCH) -> 200
        patch_payload = {
            "recipient_name": "Jane Doe Modified",
        }
        resp = self.client.patch(
            f"/api/v1/customer/addresses/{new_id}/",
            data=patch_payload,
            content_type="application/json",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["data"]["recipient_name"], "Jane Doe Modified")
        self.assertEqual(resp.json()["data"]["label"], "HQ")

        # 7. Set default -> 200
        resp = self.client.post(
            f"/api/v1/customer/addresses/{new_id}/default/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["data"]["is_default"])

        # 8. Set default alias -> 200
        resp = self.client.post(
            f"/api/v1/customer/addresses/{self.address.id}/set-default/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["data"]["is_default"])

        # 9. Delete address -> 204
        resp = self.client.delete(
            f"/api/v1/customer/addresses/{new_id}/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 204)

        # 10. Retrieve deleted address -> 404
        resp = self.client.get(
            f"/api/v1/customer/addresses/{new_id}/",
            HTTP_AUTHORIZATION=auth_header,
        )
        self.assertEqual(resp.status_code, 404)

    def test_address_repository_robustness(self):
        from infrastructure.persistence.repository.address_repository_impl import AddressRepositoryInterfaceImpl
        repo = AddressRepositoryInterfaceImpl()
        user_id = str(self.user.id)

        # 1. Malformed UUIDs handled gracefully without exception
        self.assertIsNone(repo.get_by_id("invalid-uuid", user_id))
        self.assertIsNone(repo.get_by_id(str(self.address.id), "invalid-user-uuid"))
        self.assertEqual(repo.list_by_user("invalid-uuid"), [])
        repo.clear_default("invalid-uuid")

        # 2. Audit fields on create and update
        new_addr = DomainAddress(
            user_id=user_id,
            recipient_name="Audit Tester",
            phone_number="1234567890",
            address_line_1="100 Test St",
            city="Metropolis",
            country_code="US",
        )
        saved = repo.create(new_addr, actor_id=user_id)
        self.assertIsNotNone(saved.id)

        model = UserAddress.objects.get(id=saved.id)
        self.assertEqual(str(model.created_by_id), user_id)
        self.assertEqual(str(model.updated_by_id), user_id)

        # 3. Update with another actor
        saved.recipient_name = "Audit Tester Updated"
        updated = repo.update(saved, actor_id=str(self.seller.id))
        model.refresh_from_db()
        self.assertEqual(str(model.updated_by_id), str(self.seller.id))

        # 4. Soft delete sets deleted_at and deleted_by
        repo.soft_delete(saved.id, user_id=user_id, actor_id=user_id)
        model.refresh_from_db()
        self.assertIsNotNone(model.deleted_at)
        self.assertEqual(str(model.deleted_by_id), user_id)

