from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.RegisterPage, name="register"),
    path('login', views.LoginPage, name="login"),
    path('logout', views.UserLogout, name="logout"),
    path('shop', views.shop, name="shop"),
    path('blog', views.blog, name="blog"),
    path('contact-us', views.contactus, name="contactus"),
    path('newsletter', views.newsletter, name="newsletter"),
    path('shop-detail/<int:id>/', views.shopdetail, name="shopdetail"),
    path('category-view/<int:id>/', views.categoryview, name="category-view"),
    path('cart', views.cart, name="cart"),
    path('add/<int:id>/', views.add_to_cart, name="add-to-cart"),
    path('remove/<int:id>/', views.cart_remove, name="remove-cart"),
    path('delete/<int:id>/', views.cart_delete, name="delete-cart"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('addwishlist/<int:id>/', views.add_to_wishlist, name="add-wishlist"),
    path('removewishlist/<int:id>/', views.delete_from_wishlist, name="remove-wishlist"),
    path('movecart/<int:id>/', views.move_to_cart, name="move-cart"),
    path('checkout', views.checkout, name="checkout"),
    path('my-orders', views.my_orders, name="my-orders"),
    path('my-profile', views.my_profile, name="my-profile"),
    path("update-profile/<int:id>/",views.UpdateProfile.as_view(), name="update-profile"),
    path("blog-category/<int:id>/",views.blog_category, name="blog_category"),
    path('about us', views.about, name="about"),












    

    # Password reset paths
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='forgot_password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_complete.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),


    



    



   

]
  