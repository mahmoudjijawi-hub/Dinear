from django.urls import reverse


def get_ingress_token(request):
    """استخراج توكن البروكسي من الطلب أو الجلسة"""
    token = request.GET.get('_ingress_token', '')
    if not token and hasattr(request, 'session'):
        token = request.session.get('ingress_token', '')
    return token


def append_ingress_token(url, token):
    """إضافة توكن البروكسي للرابط إن وُجد"""
    if not token or '_ingress_token=' in url:
        return url
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}_ingress_token={token}'


def redirect_with_token(request, to, *args, **kwargs):
    """إعادة توجيه مع الحفاظ على توكن البروكسي"""
    from django.shortcuts import redirect
    if isinstance(to, str) and not to.startswith('/'):
        url = reverse(to, args=args, kwargs=kwargs)
    else:
        url = to
    return redirect(append_ingress_token(url, get_ingress_token(request)))
