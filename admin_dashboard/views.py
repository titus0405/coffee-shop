import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from core.models import Admin, User, Product, Cart, Order, Booking


def _admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'admin_name' not in request.session:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            admin_user = Admin.objects.get(admin_name=username, password=password)
            request.session['admin_name'] = admin_user.admin_name
            request.session['email'] = admin_user.email
            request.session['admin_id'] = admin_user.id
            messages.success(request, 'Admin login successful!')
            return redirect('admin_dashboard')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid username or password!')
            return redirect('admin_login')
    return render(request, 'admin/login.html')


def admin_logout(request):
    if 'admin_name' in request.session:
        del request.session['admin_name']
        del request.session['email']
        del request.session['admin_id']
    return redirect('admin_login')


@_admin_required
def dashboard(request):
    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_admins': Admin.objects.count(),
        'total_users': User.objects.count(),
        'total_cart_items': Cart.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)


@_admin_required
def admins_list(request):
    admins = Admin.objects.all()
    return render(request, 'admin/admins_list.html', {'admins': admins})


@_admin_required
def create_admin(request):
    if request.method == 'POST':
        admin_name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        Admin.objects.create(admin_name=admin_name, email=email, password=password)
        messages.success(request, 'Admin created successfully!')
        return redirect('admins_list')
    return render(request, 'admin/create_admin.html')


@_admin_required
def delete_admin(request, pid):
    admin = get_object_or_404(Admin, id=pid)
    admin.delete()
    messages.success(request, 'Admin deleted successfully!')
    return redirect('admins_list')


@_admin_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'admin/products_list.html', {'products': products})


@_admin_required
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '')
        type_ = request.POST.get('type', '')
        image_file = request.FILES.get('image')

        image_path = ''
        if image_file:
            ext = os.path.splitext(image_file.name)[1].lower()
            if ext in ('.jpg', '.jpeg', '.png', '.gif'):
                filename = image_file.name.replace(' ', '_')
                upload_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                with open(upload_path, 'wb+') as dest:
                    for chunk in image_file.chunks():
                        dest.write(chunk)
                image_path = 'images/' + filename

        Product.objects.create(
            name=name,
            image=image_path,
            description=description,
            price=price,
            type=type_,
        )
        messages.success(request, 'Product created successfully!')
        return redirect('admin_products')
    return render(request, 'admin/create_product.html')


@_admin_required
def delete_product(request, pid):
    product = get_object_or_404(Product, id=pid)
    if product.image:
        img_path = os.path.join(settings.MEDIA_ROOT, product.image)
        if os.path.exists(img_path):
            os.remove(img_path)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('admin_products')


@_admin_required
def bookings_list(request):
    bookings = Booking.objects.all()
    return render(request, 'admin/bookings_list.html', {'bookings': bookings})


@_admin_required
def delete_booking(request, pid):
    booking = get_object_or_404(Booking, id=pid)
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return redirect('bookings_list')


@_admin_required
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'admin/orders_list.html', {'orders': orders})


@_admin_required
def delete_order(request, pid):
    order = get_object_or_404(Order, id=pid)
    order.delete()
    messages.success(request, 'Order deleted successfully!')
    return redirect('orders_list')


@_admin_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'admin/users_list.html', {'users': users})


@_admin_required
def delete_user(request, pid):
    user = get_object_or_404(User, id=pid)
    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('users_list')
