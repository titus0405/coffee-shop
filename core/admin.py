from django.contrib import admin
from .models import Admin, User, Product, Cart, Order, Booking

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_name', 'email', 'created_at')
    search_fields = ('admin_name', 'email')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'user_id', 'size')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'total_price', 'status', 'user_id', 'created_at')
    list_filter = ('status',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date', 'time', 'phone', 'status', 'user_id')
    list_filter = ('status',)
