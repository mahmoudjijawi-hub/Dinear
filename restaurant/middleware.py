from django.conf import settings
from django.http import HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware

from menu.utils import append_ingress_token, get_ingress_token


class CloudDevCsrfMiddleware(CsrfViewMiddleware):
    """يتعامل مع CSRF في بيئة Cursor Cloud أثناء التطوير"""

    TRUSTED_SUFFIXES = (
        '.cursorvm.com',
        '.agent.cvm.dev',
        'localhost',
        '127.0.0.1',
    )

    def _is_trusted_request(self, request):
        if not settings.DEBUG:
            return False
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


class IngressTokenMiddleware:
    """يحافظ على _ingress_token في كل إعادات التوجيه"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = get_ingress_token(request)
        if token:
            request.session['ingress_token'] = token
        else:
            token = request.session.get('ingress_token', '')

        response = self.get_response(request)
        if isinstance(response, HttpResponseRedirect) and token:
            response['Location'] = append_ingress_token(response['Location'], token)
        return response
