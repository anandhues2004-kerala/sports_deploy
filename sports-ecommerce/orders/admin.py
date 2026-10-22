from django.contrib import admin
from orders.models import Order,Orderitem



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "total_price",
        "order_status",
        "created_at",
    )

    list_filter = (
        "order_status",
        "created_at",
    )

    search_fields = (
        "owner__user__username",
    )

    list_editable = (
        "order_status",
    )


@admin.register(Orderitem)
class OrderitemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "owner",
        "product",
        "quantity",
    )

    search_fields = (
        "product__name",
        "owner__owner__user__username",
    )