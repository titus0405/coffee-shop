from .models import Cart

def cart_count(request):
    """Provide cart item count for the header across all pages."""
    count = 0
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        items = Cart.objects.filter(user_id=user_id)
        count = sum(item.quantity for item in items)
    return {'cart_count': count}
