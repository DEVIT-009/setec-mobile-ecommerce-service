from django.urls import path
from interface.address.view.address_customer_view import AddressCustomerView

urlpatterns = [
    # GET  /api/v1/customer/addresses/                      -> list
    # POST /api/v1/customer/addresses/                      -> create
    path('', AddressCustomerView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='customer-address-list-create'),

    # POST  /api/v1/customer/addresses/<uuid>/default/     -> set default
    # PATCH /api/v1/customer/addresses/<uuid>/default/     -> set default
    path('<uuid:address_id>/default/', AddressCustomerView.as_view({
        'post': 'set_default',
        'patch': 'set_default',
    }), name='customer-address-default'),

    # POST  /api/v1/customer/addresses/<uuid>/set-default/ -> set default alias
    # PATCH /api/v1/customer/addresses/<uuid>/set-default/ -> set default alias
    path('<uuid:address_id>/set-default/', AddressCustomerView.as_view({
        'post': 'set_default',
        'patch': 'set_default',
    }), name='customer-address-set-default'),

    # GET    /api/v1/customer/addresses/<uuid>/             -> retrieve
    # PUT    /api/v1/customer/addresses/<uuid>/             -> update (full)
    # PATCH  /api/v1/customer/addresses/<uuid>/             -> partial_update
    # DELETE /api/v1/customer/addresses/<uuid>/             -> destroy
    path('<uuid:address_id>/', AddressCustomerView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name='customer-address-detail'),
]
