from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns=[
    path("cart",views.show_cart,name='cart'),
    path("add_cart",views.add_to_cart,name="add_to_cart"),
    path('remove/<pk>',views.remove_item_cart,name="remove"),
    path("checkout",views.checkout_cart,name="checkout"),
    path('orderview',views.view_orders,name='view'),
     path(
        "payment/",
        views.create_payment,
        name="payment"
    ),
    path("cash-on-delivery/", views.cash_on_delivery, name="delivery"),

    path(
        "payment-success/",
        views.payment_success,
        name="payment_success"
    ),


]
