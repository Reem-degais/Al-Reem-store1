from django.shortcuts import render, redirect
from django.http import JsonResponse
from cart.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProducts
from store.models import Product
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.


def payment(request):
    #store payment details inside payment method
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID']) 
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to the product order table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct= OrderProducts()
        orderproduct.order_id = order.id
        orderproduct.quantity = item.quantity
        orderproduct.is_ordered = True
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.product_price = item.product.price
        orderproduct.save()
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProducts.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        #reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order_successful_email.html', {
        'user': request.user,
        'order': order,
    })
    email_address = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[email_address])
    send_email.send()


    #send data back to senddata method 
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, subtotal=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_counter = cart_items.count()
    if cart_counter <= 0:
        return redirect('store')
    
    subtotal = 0
    for cart_item in cart_items:
        subtotal += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = subtotal
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order= Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'subtotal': subtotal,

            }
            return render(request, 'payment.html', context)
    else:
        return redirect('checkout')
    

def order_successful(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProducts.objects.filter(order_id=order.id)

        subtotal = 0
        for item in ordered_products:
            subtotal += item.product_price * item.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'order_successful.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')