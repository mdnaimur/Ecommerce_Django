from django.db import models
from django.contrib.auth.models import User


# Create your models here.
CATEGORY_CHOICES = (
    ('CR', 'Curd'),
    ('ML', 'Milk'),
    ('LS', 'Lassi'),
    ('MS', 'Milkshake'),
    ('PN', 'Paneer'),
    ('GN', 'Ghee'),
    ('CZ', 'Cheese'),
    ('IC', 'Ice-Creams'),

)


STATE_CHOICES = (
    ("Dhaka",
     "Dhaka"),
    ("Chittagong",
     "Chittagong"),
    ("Khulna",
     "Khulna"),
    ("Rajshahi",
     "Rajshahi"),
    ("Barisal",
     "Barisal"),
    ("Sylhet",
     "Sylhet"),
    ("Rangpur",
     "Rangpur"),
    ("Comilla",
     "Comilla"),
    ("Narayanganj",
     "Narayanganj"),
    ("Gazipur",
     "Gazipur"),
    ("Mymensingh",
     "Mymensingh"),
    ("Cox's Bazar",
     "Cox's Bazar"),
    ("Jessore",
     "Jessore"),
    ("Tangail",
     "Tangail"),
    ("Feni",
     "Feni"),
    ("Pabna",
     "Pabna"),
    ("Netrokona",
     "Netrokona"),
    ("Narail",
     "Narail"),
    ("Bogura",
     "Bogura"),
    ("Pirojpur",
     "Pirojpur"),

)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name
