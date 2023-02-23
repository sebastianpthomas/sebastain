from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.conf import settings
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext



# Create your views here.

#RegisterPage
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect("login")
        else:
            return render(request, "registerpage.html", {'form':form})
    return render(request, "registerpage.html", {'form':form})


#loginpage
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "welcome " + str(request.user.username))
            return redirect('home')
        else:
            messages.info(request, "Invalid Login Credentials")
            return redirect("login")
    return render(request, "loginpage.html")


#Logout
def UserLogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully !!")
    return redirect('home')


def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        news = NewsLetter.objects.create(email=email)
        news.save()
        messages.success(request, "Thanks for Subscribing")
        return redirect('home')
    category = Category.objects.all()
    featured = Products.objects.filter(featured=True)
    top = Products.objects.filter(top_selled=True)      
    return render(request, "index.html", {"category":category, "featured":featured, "top":top})


def shop(request):
    category_list = Category.objects.all()
    if request.method == 'GET':
        pro=request.GET.get('product')
        if pro:
            try:
                products=Products.objects.filter(name__icontains=pro)
            except Products.DoesNotExist:
                return render(request,"shop.html",{"error":"No results found"})
            return render(request,"shop.html",{"products":products, "category_list":category_list})
    products = Products.objects.all()
    product_count = Products.objects.all().count()
    context = {"category_list":category_list, "product_count":product_count, "products":products}
    return render(request, "shop.html", context)

def categoryview(request, id):
    category_list = Category.objects.all()
    product_count = Products.objects.all().count()
    category = Category.objects.get(id=id)
    products = Products.objects.filter(category=category)
    context = {"products":products, "product_count":product_count, "category_list":category_list}
    return render(request, "shop.html",  context)



def contactus(request):
    if request.method =='POST':
        message = request.POST.get('message')
        print(message)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        Contact.objects.create(message=message, name=name, email=email, subject=subject)
        messages.success(request, "Thank you for contacting us !!!")
        return redirect('home')

    return render(request, "contact.html")


def blog(request):
    blogs = Blogs.objects.all()
    cat = Blogs.objects.all()
    context = {"blogs":blogs, "cat":cat}
    return render(request, "blog.html", context)


def shopdetail(request, id):
    product = Products.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        Review.objects.create(name=name,email=email, rating=rating, review=review ,product=product)
        messages.success(request, "Thanks for the review !!")
        return HttpResponseRedirect(request.path)
    reviews = product.review_set.all()
    review_count = product.review_set.all().count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    context = {"product":product, "reviews":reviews, "average_rating":average_rating, "review_count":review_count}
    return render(request, "shop-detail.html", context)

def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("hiiiiiiiiiiiii"+ email)
        NewsLetter.objects.create(email=email)
        return redirect('home')


@login_required
def add_to_cart(request, id):
    product = Products.objects.get(id=id)
    try:
        cart = Cart.objects.get(user=request.user, oredered=False)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()
    try:
        cart_item = CartItems.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Product added to cart")
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
        messages.success(request, "Product added to cart")
    return redirect('cart')


@login_required
def cart(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(user=request.user, oredered=False)
        cart_items = CartItems.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, "cart.html", {"cart_items":cart_items, "total":total, "counter":counter})


@login_required
def cart_remove(request, id):
    cart = Cart.objects.get(user=request.user, oredered=False)
    product = Products.objects.get(id=id)
    cart_item = CartItems.objects.get(cart=cart, product=product)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        messages.success(request, "Product removed from cart")
    return redirect('cart')


@login_required
def cart_delete(request, id):
    cart = Cart.objects.get(user=request.user, oredered=False)
    product = Products.objects.get(id=id)
    cart_item = CartItems.objects.get(product=product, cart=cart)
    cart_item.delete()
    messages.success(request, "Product removed from cart")
    return redirect('cart')


@login_required
def add_to_wishlist(request, id):
    product = Products.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if product not in wishlist.product.all():
        wishlist.product.add(product)
        messages.success(request, "Product added to wishlist")
    else:
        messages.success(request, "Product already in wishlist")
    return redirect('shop')


@login_required
def wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.get(user=user)
    products = wishlist.product.all()
    return render(request, 'wishlist.html', {'products': products})


@login_required
def delete_from_wishlist(request, id):
    product = Products.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.remove(product)
    messages.success(request, "Product removed from wishlist")
    return redirect('wishlist')


@login_required
def move_to_cart(request, id):
    product = Products.objects.get(id=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.product.remove(product)

    cart, created = Cart.objects.get_or_create(user=request.user, oredered=False)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, "Product moved to cart")
    return redirect('cart')


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, oredered=False)[:1].get()
    profile_details = Profile.objects.filter(user=request.user)
    cart_items = CartItems.objects.filter(cart=cart)
    total = 50
    for item in cart_items:
        total += float(item.sub_total())
    STRIPE_KEY=settings.STRIPE_PUBLISHABLE_KEY
    context = {
        'cart_items': cart_items,
        'total': total,
        'STRIPE_PUBLIC_KEY':STRIPE_KEY,
        'profile_details':profile_details,
    }
    return render(request, 'checkout.html', context)


def my_orders(request):
    orders = Cart.objects.filter(user=request.user, oredered=True)
    # orders = CartItems.objects.filter(cart=cart)
    return render(request, "my-orders.html", {"orders":orders})


def my_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        add_1 = request.POST.get('add_1')
        add_2 = request.POST.get('add_2')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        profile = Profile.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email, add_1=add_1, add_2=add_2, city=city, country=country, zip_code=zip_code, user=request.user)
        messages.success(request, "Profile created successfully !!!!")
        return redirect('home')
 
    profile_details = Profile.objects.filter(user=request.user)
    if profile_details:
        return render(request, "my-profile.html", {"profile_details":profile_details})
    else:
        return render(request, "my-profile.html")



class UpdateProfile(UpdateView):
    model = Profile
    pk_url_kwarg = "id"
    template_name = "update-profile.html"
    success_url = reverse_lazy("my-profile")
    form_class = UpdateProfileForm

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        # text = _("hello")
    finally:
        activate(cur_language)
        # return text

def blog_category(request, id):
    blog = Blogs.objects.get(id=id)
    cat = Blogs.objects.all()
    category = blog.category
    blogs = Blogs.objects.filter(category=category)
    return render(request, "blog.html", {"blogs":blogs, "cat":cat})

def about(request):
    return render(request,"about.html")