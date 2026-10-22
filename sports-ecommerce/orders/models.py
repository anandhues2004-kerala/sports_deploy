from django.db import models
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,"live"),(DELETE,"delete"))
    CART_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    OREDR_DELIVERD=3
    ORDER_REJETED=4
    STATUS_CHOICE=((ORDER_PROCESSED,"ORDER_PROCESSED"),
                   (OREDR_DELIVERD," OREDR_DELIVERD"),
                   (ORDER_REJETED," ORDER_REJETED"),
                   (CART_STAGE, "Cart"),
                    (ORDER_CONFIRMED, "Order Confirmed")
                   )
    razorpay_order_id=models.CharField(max_length=200,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=200,blank=True,null=True)
    razorpay_signature=models.CharField(max_length=500,blank=True,null=True)
    payment_status=models.CharField(max_length=20,default="pending")
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=0)
    total_price=models.FloatField(default=0)
    owner=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name="orders")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    delete_status=models.IntegerField(choices= DELETE_CHOICES,default=LIVE)
    def __str__(self) ->str:
        return "order-{}-{}".format(self.id,self.owner.user.username)

class Orderitem(models.Model):
    product=models.ForeignKey(Product,related_name="added_cart",on_delete=models.SET_NULL,null=True)  
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="added_items")

    def __str__(self) ->str:
            return "{}".format(self.owner)



