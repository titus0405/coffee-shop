from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('book-table/', views.book_table, name='book_table'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # User dashboard
    path('user-profile/', views.user_profile, name='user_profile'),
    path('your-orders/', views.your_orders, name='your_orders'),

    # Products / Cart / Checkout
    path('product-single/<int:pid>/', views.product_single, name='product_single'),
    path('add-to-cart/<int:pid>/', views.product_single, name='add_to_cart'),
    path('remove-from-cart/<int:pid>/', views.delete_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('pay/<int:oid>/', views.pay, name='pay'),
]
