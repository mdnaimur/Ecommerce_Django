from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.contrib import messages
from . models import Product, Customer
from . forms import CustomerRegistrationFrom, CustomerProfileForm
# Create your views here.


def home(request):
    return render(request, 'basic/home.html')


def about(request):
    return render(request, 'basic/about.html')


def contact(request):
    return render(request, 'basic/contact.html')


class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values(
            'title')
        return render(request, "basic/category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values(
            'title')
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
