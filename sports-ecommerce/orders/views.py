
from django.shortcuts import render, redirect
from orders.models import Order, Orderitem
from products.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.conf import settings



client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)
@login_required
def create_payment(request):

    user = request.user

    try:
        customer = user.customer_profile
    except ObjectDoesNotExist:
        messages.error(request, "No profile found for your account")
        return redirect("signup")

    # Get user's cart
    cart_obj = Order.objects.get(
        owner=customer,
        order_status=Order.CART_STAGE
    )

    # Get total amount
    amount = float(request.POST.get("total", 0))

    # Convert rupees to paise
    amount_paise = int(amount * 100)

    if amount_paise < 100:
        messages.error(request, "Invalid order amount.")
        return redirect("cart")

    # Create Razorpay order
    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": f"order_{cart_obj.id}",
    })

    # Save Razorpay order ID
    cart_obj.razorpay_order_id = razorpay_order["id"]
    cart_obj.total_price = amount
    cart_obj.save()

    context = {
        "cart": cart_obj,
        "razorpay_order": razorpay_order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount_paise,
    }

    return render(request, "payment.html", context)


@login_required
def payment_success(request):

    payment_id = request.GET.get("payment_id")
    order_id = request.GET.get("order_id")
    signature = request.GET.get("signature")

    try:

        # Verify Razorpay payment
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

        user = request.user
        customer = user.customer_profile

        # Get cart
        cart_obj = Order.objects.get(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Save Razorpay details
        cart_obj.razorpay_order_id = order_id
        cart_obj.razorpay_payment_id = payment_id
        cart_obj.razorpay_signature = signature

        # Change payment and order status
        cart_obj.payment_status = "Paid"
        cart_obj.order_status = Order.ORDER_CONFIRMED

        cart_obj.save()

        messages.success(
            request,
            "Payment successful! Your order has been confirmed."
        )

        return redirect("view")

    except Exception as e:

        print("Payment Error:", e)

        messages.error(
            request,
            "Payment verification failed."
        )

        return redirect("cart")
@login_required
def cash_on_delivery(request):

    customer = request.user.customer_profile

    cart, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )


    if not cart.added_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    
    total = sum(
        item.product.price * item.quantity
        for item in cart.added_items.all()
    )


    cart.total_price = total
    cart.order_status = Order.ORDER_CONFIRMED
    cart.payment_status = "COD"
    cart.save()

    messages.success(
        request,
        "Order placed successfully!"
    )

    return redirect("cart")


def show_cart(request):
    user = request.user
    try:
        customer = user.customer_profile
    except ObjectDoesNotExist:
        messages.error(request,"No profile found your account")  
        return redirect("index") 
    cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
    )

    context = {
             "cart": cart_obj
    }

    return render(request, "cart.html", context)


def add_to_cart(request):

    if request.method == "POST":

        user = request.user
        try:
            customer = user.customer_profile
        except(ObjectDoesNotExist,AttributeError):
            messages.error(request,"No profile found for your account")
            return redirect("signup")    

        quantity = int(request.POST.get("quantity", 1))
        product_id = request.POST.get("product_id")

        # Get or create cart
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Get product
        product = Product.objects.get(pk=product_id)

        # Get or create order item
        ordered_item, created = Orderitem.objects.get_or_create(
            product=product,
            owner=cart_obj
        )

        # If product already exists, increase quantity
        if created:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity

        ordered_item.save()

    return redirect("cart")
def remove_item_cart(request,pk):
    item=Orderitem.objects.get(pk=pk)
    if item:
        item.delete()
        return redirect('cart')

    
def checkout_cart(request):
    if request.method == "POST":
        try:    
            user = request.user
            customer = user.customer_profile
            total=float(request.POST.get("total"))
            order_obj= Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            ) 
            if order_obj:  
                order_obj.order_status=Order.ORDER_CONFIRMED 
                order_obj.total_price=total
                order_obj.save()
                status_message="Your order under Processed"    
                messages.success(request,status_message)
            else:
                status_message="unable to processed"    
                messages.error(request,status_message)    
        except Exception as e:
            status_message="unable to processed"    
            messages.error(request,status_message)
    return redirect("cart")  




@login_required(login_url='signup')
def view_orders(request):
    user=request.user
    customer=user.customer_profile
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={"orders":all_orders}
    return render(request,"orders.html",context)
          




    
    
        


