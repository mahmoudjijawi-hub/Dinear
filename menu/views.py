import json
from decimal import Decimal, InvalidOperation

from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .decorators import staff_required
from .models import Category, Order, OrderItem, Product


@ensure_csrf_cookie
def menu_view(request):
    """عرض صفحة المنيو الرئيسية"""
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'menu/menu.html', {'categories': categories})


@require_POST
def place_order(request):
    """استقبال الطلب وحفظه بقاعدة البيانات"""
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        if not items:
            return JsonResponse({'success': False, 'error': 'السلة فارغة'}, status=400)

        total = Decimal('0')
        order_items_data = []

        for item in items:
            product_id = item.get('product_id')
            quantity = int(item.get('quantity', 0))
            if quantity <= 0:
                continue

            try:
                product = Product.objects.get(pk=product_id, is_available=True)
            except Product.DoesNotExist:
                return JsonResponse(
                    {'success': False, 'error': f'المنتج غير متوفر: {product_id}'},
                    status=400,
                )

            subtotal = product.price * quantity
            total += subtotal
            order_items_data.append({
                'product': product,
                'product_name': product.name,
                'quantity': quantity,
                'unit_price': product.price,
                'subtotal': subtotal,
            })

        if not order_items_data:
            return JsonResponse({'success': False, 'error': 'السلة فارغة'}, status=400)

        order = Order.objects.create(total=total)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'total': str(total),
            'items': [
                {
                    'name': i['product_name'],
                    'quantity': i['quantity'],
                    'unit_price': str(i['unit_price']),
                    'subtotal': str(i['subtotal']),
                }
                for i in order_items_data
            ],
        })

    except (json.JSONDecodeError, ValueError, InvalidOperation, TypeError):
        return JsonResponse({'success': False, 'error': 'بيانات الطلب غير صالحة'}, status=400)


@ensure_csrf_cookie
def dashboard_login(request):
    """صفحة تسجيل دخول صاحب المطعم"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_orders')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_orders')
        error = 'اسم المستخدم أو كلمة المرور غير صحيحة'

    return render(request, 'menu/dashboard/login.html', {'error': error})


@login_required(login_url='/dashboard/login/')
def dashboard_logout(request):
    """تسجيل خروج صاحب المطعم"""
    logout(request)
    return redirect('dashboard_login')


@staff_required
def dashboard_orders(request):
    """صفحة الطلبات الواردة"""
    status_filter = request.GET.get('status', 'all')
    orders = Order.objects.prefetch_related('items').all()

    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    return render(request, 'menu/dashboard/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.Status.choices,
    })


@staff_required
@require_POST
def update_order_status(request, order_id):
    """تحديث حالة الطلب"""
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        valid_statuses = [s[0] for s in Order.Status.choices]
        if new_status not in valid_statuses:
            return JsonResponse({'success': False, 'error': 'حالة غير صالحة'}, status=400)

        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'status': order.status,
            'status_display': order.get_status_display(),
        })
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الطلب غير موجود'}, status=404)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'success': False, 'error': 'بيانات غير صالحة'}, status=400)
