from django.shortcuts import render
from django.views import View
from django.db.models import Count
from . models import Product
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
