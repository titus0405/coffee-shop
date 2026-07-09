from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.models import Admin, User, Product, Cart, Order, Booking


def index(request):
    coffee_products = Product.objects.filter(type='coffee')
    return render(request, 'core/index.html', {'coffee_products': coffee_products})


def menu(request):
    desserts = Product.objects.filter(type='dessert')
    drinks = Product.objects.filter(type='drink')
    starters = Product.objects.filter(type='starter')
    main_dishes = Product.objects.filter(type='main dish')
    coffee_products = Product.objects.filter(type='coffee')
    return render(request, 'core/menu.html', {
        'desserts': desserts,
        'drinks': drinks,
        'starters': starters,
        'main_dishes': main_dishes,
        'coffee_products': coffee_products,
        'menu_active': True,
    })


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def services(request):
    return render(request, 'core/services.html')


@require_POST
def book_table(request):
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    date = request.POST.get('date', '')
    time = request.POST.get('time', '')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message', '')

    Booking.objects.create(
        first_name=first_name,
        last_name=last_name,
        date=date,
        time=time,
        phone=phone,
        message=message,
        user_id=request.session.get('user_id', 0),
    )
    messages.success(request, 'Booking submitted successfully!')
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['user_id'] = user.id
            messages.success(request, 'Login successful!')
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')
    return render(request, 'core/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password1', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')

        User.objects.create(
            username=username,
            email=email,
            password=password,
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    return render(request, 'core/register.html')


def logout_view(request):
    request.session.flush()
    return redirect('index')


def user_profile(request):
    if 'user_id' not in request.session:
        return redirect('login')
    bookings = Booking.objects.filter(user_id=request.session['user_id'])
    return render(request, 'core/user_profile.html', {'bookings': bookings})


def your_orders(request):
    if 'user_id' not in request.session:
        return redirect('login')
    orders = Order.objects.filter(user_id=request.session['user_id'])
    return render(request, 'core/your_orders.html', {'orders': orders})


def product_single(request, pid):
    product = get_object_or_404(Product, id=pid)
    related_products = Product.objects.filter(type=product.type).exclude(id=pid)

    if request.method == 'POST' and 'user_id' in request.session:
        name = request.POST.get('name', product.name)
        image = request.POST.get('image', product.image)
        price = request.POST.get('price', product.price)
        description = request.POST.get('description', product.description)
        size = request.POST.get('size', 'Medium')
        quantity = request.POST.get('quantity', 1)

        # Check if already in cart
        existing = Cart.objects.filter(
            product_id=pid,
            user_id=request.session['user_id'],
        ).first()
        if existing:
            messages.info(request, 'Product already in cart!')
        else:
            Cart.objects.create(
                name=name,
                image=image,
                price=price,
                description=description,
                product_id=pid,
                size=size,
                quantity=int(quantity),
                user_id=request.session['user_id'],
            )
            messages.success(request, 'Product added to cart!')

        return redirect(request.META.get('HTTP_REFERER', 'index'))

    in_cart = False
    if 'user_id' in request.session:
        in_cart = Cart.objects.filter(
            product_id=pid,
            user_id=request.session['user_id'],
        ).exists()

    return render(request, 'core/product_single.html', {
        'product': product,
        'related_products': related_products,
        'in_cart': in_cart,
    })


def cart_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        price_total = request.POST.get('price_total', 0)
        request.session['total_price'] = price_total
        return redirect('checkout')

    cart_items = Cart.objects.filter(user_id=request.session['user_id'])

    subtotal = 0
    for item in cart_items:
        item_total = float(item.price.replace('.', '')) * item.quantity
        item.total_price = item_total
        subtotal += item_total

    delivery = 5.00
    discount = 3.00
    total = subtotal + delivery - discount

    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery': delivery,
        'discount': discount,
        'total': total,
    })


def checkout(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    cart_items = Cart.objects.filter(user_id=user_id)

    subtotal = sum(float(item.price.replace('.', '')) * item.quantity for item in cart_items)
    delivery = 5.00
    discount = 3.00
    total = subtotal + delivery - discount

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        country = request.POST.get('country', '')
        street_address = request.POST.get('street_address', '')
        town = request.POST.get('town', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        total_price = int(total)

        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            country=country,
            street_address=street_address,
            town=town,
            zip_code=zip_code,
            phone=phone,
            email=email,
            user_id=user_id,
            status='pending',
            total_price=total_price,
        )

        Cart.objects.filter(user_id=user_id).delete()

        messages.success(request, 'Order placed successfully!')
        return redirect('pay', oid=order.id)

    return render(request, 'core/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


def pay(request, oid):
    if 'user_id' not in request.session:
        return redirect('login')
    order = get_object_or_404(Order, id=oid)
    total_price = order.total_price
    return render(request, 'core/pay.html', {'total_price': total_price, 'order': order})


def delete_cart(request, pid):
    if 'user_id' not in request.session:
        return redirect('login')
    cart_item = get_object_or_404(Cart, id=pid)
    cart_item.delete()
    return redirect('cart')


def delete_product(request, pid):
    if 'user_id' not in request.session:
        return redirect('login')
    Cart.objects.filter(product_id=pid, user_id=request.session['user_id']).delete()
    return redirect('cart')
