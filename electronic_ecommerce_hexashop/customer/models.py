from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blogs(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")
    desc = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    options = (
        ("unread", "unread"),
        ("viewed", "viewed"),
    )
    status = models.CharField(max_length=20, choices=options, default="unread")
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/")
    desc = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50)
    featured = models.BooleanField(default=False)
    top_selled = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_1 = models.ImageField(upload_to="images/")
    image_2 = models.ImageField(upload_to="images/")
    image_3 = models.ImageField(upload_to="images/")
    image_4 = models.ImageField(upload_to="images/")
    price = models.FloatField()
    available = models.BooleanField(default=True)
    desc = models.CharField(max_length=200)
    information = models.TextField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    material = models.CharField(max_length=50)
    benefits = models.TextField()
    quality_check = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oredered = models.BooleanField(default=False)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def sub_total(self):
        return '{}'.format (self.product.price * self.quantity)

    # def __str__(self):
    #     return self.product


class Wishlist(models.Model):
    product= models.ManyToManyField(Products)
    options = (
        ("Wishlisted", "Wishlisted"),
        ("in-cart", "in-cart")
        
    )
    status = models.CharField(max_length=300, choices=options, default="Wishlisted")
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)


class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    review = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.rating} stars'


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    add_1 = models.CharField(max_length=100)
    add_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name











