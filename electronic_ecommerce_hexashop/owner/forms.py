from django import forms
from django.forms import ModelForm
from customer.models import *


#Category
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class UpdateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


#Products
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


#Blogs
class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = '__all__'


class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = '__all__'