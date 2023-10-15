from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.contrib import messages
from . models import Product, Customer, Cart, Payment, OrderPlaced
from . forms import CustomerRegistrationFrom, CustomerProfileForm
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings
# Create your views here.


def home(request):
    totoalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'basic/home.html', locals())


def about(request):
    totoalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'basic/about.html', locals())


def contact(request):
    totoalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'basic/contact.html', locals())


class CategoryView(View):
    def get(self, request, val):
        totoalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        products = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values(
            'title')
        return render(request, "basic/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values(
            'title')
        totoalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, "basic/category.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "product/productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationFrom()
        return render(request, 'basic/customerregistraion.html', locals())

    def post(self, request):
        form = CustomerRegistrationFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Congratulations! User Register Successfully")
            return redirect(request, 'login', locals())
        else:
            messages.warning(request, "Invalid Input Data")
            return render(request, 'basic/customerregistraion.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'basic/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality,
                           city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Save Successfully!!')
        else:
            messages.warning(request, 'Invalid Input Data!! Try again')
        return render(request, 'basic/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'basic/address.html', locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'basic/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile Update Successfully")
        else:
            messages.warning(request, 'Invalid Input Data!! Try again')
        return redirect("address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount+value
    totalamount = amount + 40
    return render(request, 'product/adtocart.html', locals())


def plus_cart(request):
    print('I am working ')
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.discounted_price
            amount = amount+value
        totalamount = amount+40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(Data)


class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount+value
        totalamount = famount + 40
        razoramount = int(totalamount*100)
        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = {"amount": razoramount, "currency": "BDT",
                "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
      #  test = {'id': 'order_MoMjDCTdxkF9T6', 'entity': 'order', 'amount': 8500, 'amount_paid': 0, 'amount_due': 8500, 'currency': 'BDT', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1697347353}

        # print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user, amount=totalamount, razorpay_order_id=order_id, razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'product/checkout.html', locals())


def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    custoemr = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=custoemr, product=c.product,
                    quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('orders')


def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'product/orders.html', locals())


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.discounted_price
            amount = amount+value
        totalamount = amount+40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(Data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.discounted_price
            amount = amount+value
        totalamount = amount+40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(Data)
