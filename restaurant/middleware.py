from django.conf import settings
from django.http import HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware

from menu.auth_utils import append_auth_token, authenticate_token, get_auth_token
from menu.utils import append_ingress_token, get_ingress_token


class CloudDevCsrfMiddleware(CsrfViewMiddleware):
    """يتعامل مع CSRF في بيئات التطوير السحابية وRender"""

    TRUSTED_SUFFIXES = (
        '.cursorvm.com',
        '.agent.cvm.dev',
        '.onrender.com',
        'localhost',
        '127.0.0.1',
    )

    def _is_trusted_request(self, request):
        values = [
            request.get_host(),
            request.META.get('HTTP_ORIGIN', ''),
            request.META.get('HTTP_REFERER', ''),
        ]
        return any(
            value and any(suffix in value for suffix in self.TRUSTED_SUFFIXES)
            for value in values
        )

    def process_request(self, request):
        if self._is_trusted_request(request):
            request.csrf_processing_done = True
            return None
        return super().process_request(request)

    def _origin_verified(self, request):
        if self._is_trusted_request(request):
            return True
        return super()._origin_verified(request)


class DashboardAuthMiddleware:
    """مصادقة لوحة التحكم عبر توكن بالرابط — بدون الاعتماد على كوكيز الجلسة"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/'):
            user = authenticate_token(request)
            if user:
                request.user = user
                request._cached_user = user
        return self.get_response(request)


class IngressTokenMiddleware:
    """يحافظ على التوكنات في كل إعادات التوجيه"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseRedirect):
            location = response['Location']
            ingress = get_ingress_token(request)
            auth = get_auth_token(request)
            if ingress:
                location = append_ingress_token(location, ingress)
            if auth:
                location = append_auth_token(location, auth)
            response['Location'] = location
        return response
