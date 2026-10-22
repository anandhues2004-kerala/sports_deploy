from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .import views
urlpatterns=[
    path("",views.index,name="index"),
    path("products/",views.list_products,name="list_products"),
    path("productdetails<pk>",views.product_detail,name="product_detail")
]