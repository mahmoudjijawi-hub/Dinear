from django.contrib.auth.models import User
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

SIGNER = TimestampSigner(salt='dinear-dashboard-auth')
TOKEN_PARAM = 'auth_token'
TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # أسبوع


def create_auth_token(user):
    """إنشاء توكن مصادقة موقّع"""
    return SIGNER.sign(str(user.pk))


def get_auth_token(request):
    """استخراج توكن المصادقة من الطلب"""
    return request.GET.get(TOKEN_PARAM, '')


def get_user_from_token(token):
    """التحقق من التوكن وإرجاع المستخدم"""
    user_id = SIGNER.unsign(token, max_age=TOKEN_MAX_AGE)
    return User.objects.get(pk=int(user_id), is_staff=True)


def authenticate_token(request):
    """مصادقة المستخدم من التوكن — يُرجع المستخدم أو None"""
    token = get_auth_token(request)
    if not token:
        return None
    try:
        return get_user_from_token(token)
    except (BadSignature, SignatureExpired, User.DoesNotExist, ValueError, TypeError):
        return None


def append_auth_token(url, token):
    """إضافة توكن المصادقة للرابط"""
    if not token or f'{TOKEN_PARAM}=' in url:
        return url
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}{TOKEN_PARAM}={token}'
