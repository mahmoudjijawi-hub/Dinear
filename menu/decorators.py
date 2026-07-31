from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def staff_required(view_func):
    """يتحقق من تسجيل الدخول وأن المستخدم staff"""
    @wraps(view_func)
    @login_required(login_url='/dashboard/login/')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('غير مصرح لك بالوصول إلى هذه الصفحة.')
        return view_func(request, *args, **kwargs)
    return wrapper
