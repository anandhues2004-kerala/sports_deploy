from django import template
register=template.Library()
@register.simple_tag(name="total")
def total(cart):
    total=0
    for i in cart.added_items.all():
        total+=i.quantity*i.product.price
    return total    