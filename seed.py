import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Admin, User, Product

# Create admin user
if not Admin.objects.filter(admin_name='admin').exists():
    Admin.objects.create(
        admin_name='admin',
        email='admin@nscoffee.com',
        password='admin123',
    )
    print('Admin user created: admin / admin123')
else:
    print('Admin user already exists')

# Create regular user
if not User.objects.filter(username='john').exists():
    User.objects.create(
        username='john',
        email='john@example.com',
        password='password123',
    )
    print('Test user created: john / password123')
else:
    print('Test user already exists')

# Seed products
products_data = [
    # Coffee
    {'name': 'Americano', 'price': '12.00', 'type': 'coffee', 'description': 'Classic Americano coffee', 'image': 'images/menu-1.jpg'},
    {'name': 'Cappuccino', 'price': '15.00', 'type': 'coffee', 'description': 'Rich cappuccino with foam', 'image': 'images/menu-2.jpg'},
    {'name': 'Espresso', 'price': '10.00', 'type': 'coffee', 'description': 'Strong espresso shot', 'image': 'images/menu-3.jpg'},
    {'name': 'Latte', 'price': '14.00', 'type': 'coffee', 'description': 'Smooth latte with milk', 'image': 'images/menu-4.jpg'},
    # Drinks
    {'name': 'Fresh Orange Juice', 'price': '8.00', 'type': 'drink', 'description': 'Freshly squeezed orange juice', 'image': 'images/drink-1.jpg'},
    {'name': 'Iced Tea', 'price': '6.00', 'type': 'drink', 'description': 'Refreshing iced tea', 'image': 'images/drink-2.jpg'},
    {'name': 'Smoothie', 'price': '9.00', 'type': 'drink', 'description': 'Fruit smoothie', 'image': 'images/drink-3.jpg'},
    # Desserts
    {'name': 'Chocolate Cake', 'price': '7.00', 'type': 'dessert', 'description': 'Rich chocolate cake', 'image': 'images/dessert-1.jpg'},
    {'name': 'Cheesecake', 'price': '8.00', 'type': 'dessert', 'description': 'Creamy cheesecake', 'image': 'images/dessert-2.jpg'},
    {'name': 'Tiramisu', 'price': '9.00', 'type': 'dessert', 'description': 'Classic Italian tiramisu', 'image': 'images/dessert-5.jpg'},
    # Main dishes
    {'name': 'Chicken Burger', 'price': '11.00', 'type': 'main dish', 'description': 'Grilled chicken burger', 'image': 'images/burger-1.jpg'},
    {'name': 'Beef Burger', 'price': '13.00', 'type': 'main dish', 'description': 'Juicy beef burger', 'image': 'images/burger-3.jpg'},
]

for pdata in products_data:
    if not Product.objects.filter(name=pdata['name']).exists():
        Product.objects.create(**pdata)
        print(f"Product created: {pdata['name']}")
    else:
        print(f"Product already exists: {pdata['name']}")

print('\nSeed complete!')
