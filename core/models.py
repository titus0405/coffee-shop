from django.db import models

class Admin(models.Model):
    admin_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'admins'
    def __str__(self):
        return self.admin_name

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=400)
    description = models.TextField()
    price = models.CharField(max_length=5)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'products'
    def __str__(self):
        return self.name

class Cart(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    description = models.TextField()
    product_id = models.IntegerField()
    size = models.CharField(max_length=30)
    quantity = models.IntegerField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'cart'
    def __str__(self):
        return f"{self.name} x{self.quantity}"

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    town = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    user_id = models.IntegerField()
    status = models.CharField(max_length=20)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'orders'
    def __str__(self):
        return f"Order #{self.id}"

class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date = models.CharField(max_length=11)
    time = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'bookings'
    def __str__(self):
        return f"Booking #{self.id}"
