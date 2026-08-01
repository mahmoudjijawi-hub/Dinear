from .auth_utils import get_auth_token
from .utils import get_ingress_token


def dashboard_tokens(request):
    """إتاحة التوكنات في قوالب لوحة التحكم"""
    return {
        'auth_token': get_auth_token(request),
        'ingress_token': get_ingress_token(request),
    }
