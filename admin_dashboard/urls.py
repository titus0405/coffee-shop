from django.urls import path
from . import views

urlpatterns = [
    # Admin auth
    path('', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    # Admins management
    path('admins/', views.admins_list, name='admins_list'),
    path('admins/create/', views.create_admin, name='create_admin'),
    path('admins/delete/<int:admin_id>/', views.delete_admin, name='delete_admin'),

    # Products management
    path('products/', views.products_list, name='admin_products'),
    path('products/create/', views.create_product, name='create_product'),

    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Bookings
    path('bookings/', views.bookings_list, name='bookings_list'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),

    # Orders
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),

    # Users management
    path('users/', views.users_list, name='users_list'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
