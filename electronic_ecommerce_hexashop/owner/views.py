from django.shortcuts import render, redirect
from customer.models import *
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .decorators import signin_required
from .forms import *


# Create your views here.
@signin_required
def dashboard(request):
    return render(request, "dashboard.html")


#Category
@signin_required
def ManageCategory(request):
    category = Category.objects.all()
    context = {"category":category}
    return render(request, "manage-category.html", context)


@signin_required
def AddCategory(request):
    form = AddCategoryForm()
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully !!")
            return redirect('manage-category')
    return render(request, "add-category.html", {"form":form})


@method_decorator(signin_required,name="dispatch")
class UpdateCategory(UpdateView):
    model = Category
    pk_url_kwarg = "id"
    template_name = "update-category.html"
    success_url = reverse_lazy("manage-category")
    form_class = UpdateCategoryForm

    def form_valid(self, form):
        messages.success(self.request, "Category  updated successfully")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class DeleteCategory(DeleteView):
    model = Category
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-category")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Category deleted successfully")
        return super(DeleteCategory, self).form_valid(form)


#Products
@signin_required
def ManageProducts(request):
    products = Products.objects.all()
    context = {"products":products}
    return render(request, "manage-products.html", context)


@signin_required
def AddProduct(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully !!")
            return redirect('manage-products')
    return render(request, "add-product.html", {"form":form})


@method_decorator(signin_required,name="dispatch")
class UpdateProduct(UpdateView):
    model = Products
    pk_url_kwarg = "id"
    template_name = "update-product.html"
    success_url = reverse_lazy("manage-products")
    form_class = UpdateProductForm

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class DeleteProduct(DeleteView):
    model = Products
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-products")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Product deleted successfully")
        return super(DeleteProduct, self).form_valid(form)


#Blogs
@signin_required
def ManageBlogs(request):
    blogs = Blogs.objects.all()
    context = {"blogs":blogs}
    return render(request, "manage-blogs.html", context)


@signin_required
def AddBlog(request):
    form = AddBlogForm()
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog added successfully !!")
            return redirect('manage-blogs')
    return render(request, "add-blog.html", {"form":form})


@method_decorator(signin_required,name="dispatch")
class UpdateBlog(UpdateView):
    model = Blogs
    pk_url_kwarg = "id"
    template_name = "update-blog.html"
    success_url = reverse_lazy("manage-blogs")
    form_class = UpdateBlogForm

    def form_valid(self, form):
        messages.success(self.request, "Blog updated successfully")
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class DeleteBlog(DeleteView):
    model = Blogs
    pk_url_kwarg = "id"
    success_url = reverse_lazy("manage-blogs")
    template_name = "confirm-delete.html"

    def form_valid(self, form):
        messages.success(self.request, "Blog deleted successfully")
        return super(DeleteBlog, self).form_valid(form)


#Subscribe
@signin_required
def ManageSubscribe(request):
    subscribe = NewsLetter.objects.all()
    context = {"subscribe":subscribe}
    return render(request, "manage-subscribe.html", context)


#Enquiries
@signin_required
def ManageEnquiries(request):
    enquiry = Contact.objects.all()
    enquiry_count = Contact.objects.filter(status="unread").count()
    context = {"enquiry":enquiry, "enquiry_count":enquiry_count}
    return render(request, "manage-enquiry.html", context)


@signin_required
def ViewEnquiry(request, id):
    enquiry = Contact.objects.get(id=id)
    if enquiry.status == "unread":
        enquiry.status = "viewed"
        enquiry.save()
    return render(request, "view-enquiry.html", {"enquiry":enquiry})