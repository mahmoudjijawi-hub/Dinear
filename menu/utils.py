from django.urls import reverse

from .auth_utils import append_auth_token, get_auth_token


def get_ingress_token(request):
    """استخراج توكن البروكسي من الطلب"""
    return request.GET.get('_ingress_token', '')


def append_ingress_token(url, token):
    """إضافة توكن البروكسي للرابط إن وُجد"""
    if not token or '_ingress_token=' in url:
        return url
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}_ingress_token={token}'


def append_query_tokens(url, request, auth_token=None):
    """إضافة كل التوكنات المطلوبة للرابط"""
    url = append_ingress_token(url, get_ingress_token(request))
    token = auth_token or get_auth_token(request)
    if token:
        url = append_auth_token(url, token)
    return url


def redirect_with_token(request, to, auth_token=None, *args, **kwargs):
    """إعادة توجيه مع الحفاظ على توكنات البروكسي والمصادقة"""
    from django.shortcuts import redirect
    if isinstance(to, str) and not to.startswith('/'):
        url = reverse(to, args=args, kwargs=kwargs)
    else:
        url = to
    return redirect(append_query_tokens(url, request, auth_token=auth_token))
