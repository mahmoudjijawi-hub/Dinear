from functools import wraps

from django.http import HttpResponseForbidden

from .utils import redirect_with_token


def staff_required(view_func):
    """يتحقق من المصادقة (توكن أو جلسة) وأن المستخدم staff"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect_with_token(request, 'dashboard_login')
        if not request.user.is_staff:
            return HttpResponseForbidden('غير مصرح لك بالوصول إلى هذه الصفحة.')
        return view_func(request, *args, **kwargs)
    return wrapper
