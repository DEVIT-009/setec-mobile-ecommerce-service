from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/users/', include('interface.user.url.user_url')),

    re_path(r'^api/v1/legacy-auth/?', include('shared.security.auth_url')),
    re_path(r'^api/v1/auth/?', include('interface.auth.url.auth_url')),

    path('api/v1/', include('interface.category.url.category_url')),
    path('api/v1/', include('interface.store.url.store_url')),
    path('api/v1/', include('interface.product.url.product_url')),
    path('api/v1/', include('interface.product.url.product_variant_url')),
    path('api/v1/', include('interface.product.url.variant_option_url')),
    
    path('api/v1/public/', include('interface.home.url.home_url')),
    path('api/v1/public/', include('interface.tag.url.tag_public_url')),
    path('api/v1/public/', include('interface.legal_document.url.legal_document_url')),
    path('api/v1/public/', include('interface.review.url.review_url')),

    path('api/v1/customer/addresses/', include('interface.address.url.address_url')),
    path('api/v1/customer/orders/', include('interface.order.url.order_url')),
    path('api/v1/customer/shipments/', include('interface.shipment.url.shipment_url')),
    path('api/v1/customer/search-history/', include('interface.search_history.url.search_history_url')),
    path('api/v1/customer/favorites/', include('interface.favorite.url.favorite_url')),
    path('api/v1/customer/cart/', include('interface.cart.url.cart_url')),
    path('api/v1/customer/conversations/', include('interface.conversation.url.conversation_url')),
    path('api/v1/customer/messages/', include('interface.conversation.url.message_url')),
    path('api/v1/customer/notifications/', include('interface.notification.url.notification_url')),
    path('api/v1/customer/support/', include('interface.support_ticket.url.support_ticket_url')),
    path('api/v1/customer/legal-documents/', include('interface.legal_document.url.legal_document_customer_url')),
    path('api/v1/customer/uploads/', include('interface.upload.url.upload_url')),

    path('api/v1/admin/', include('interface.tag.url.tag_admin_url')),
    path('api/v1/admin/', include('interface.order.url.order_admin_url')),
    path('api/v1/admin/', include('interface.shipment.url.shipment_admin_url')),
    path('api/v1/admin/', include('interface.review.url.review_admin_url')),
    path('api/v1/admin/', include('interface.notification.url.notification_admin_url')),
    path('api/v1/admin/', include('interface.support_ticket.url.support_ticket_admin_url')),
    path('api/v1/admin/', include('interface.legal_document.url.legal_document_admin_url')),
]
