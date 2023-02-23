from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path("manage-category",views.ManageCategory, name="manage-category"),
    path("add-category",views.AddCategory, name="add-category"),
    path("update-category/<int:id>/",views.UpdateCategory.as_view(), name="update-category"),
    path("delete-category/<int:id>/",views.DeleteCategory.as_view(), name="delete-category"),
    path("manage-products",views.ManageProducts, name="manage-products"),
    path("add-product",views.AddProduct, name="add-product"),
    path("update-product/<int:id>/",views.UpdateProduct.as_view(), name="update-product"),
    path("delete-product/<int:id>/",views.DeleteProduct.as_view(), name="delete-product"),
    path("manage-blogs",views.ManageBlogs, name="manage-blogs"),
    path("add-blog",views.AddBlog, name="add-blog"),
    path("update-blog/<int:id>/",views.UpdateBlog.as_view(), name="update-blog"),
    path("delete-blog/<int:id>/",views.DeleteBlog.as_view(), name="delete-blog"),
    path("manage-subscribe",views.ManageSubscribe, name="manage-subscribe"),
    path("manage-enquiries",views.ManageEnquiries, name="manage-enquiries"),
    path("view-enquiry/<int:id>/",views.ViewEnquiry, name="view-enquiry"),
    




]