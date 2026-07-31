from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware


class CloudDevCsrfMiddleware(CsrfViewMiddleware):
    """يسمح بطلبات POST من نطاقات Cursor Cloud أثناء التطوير"""

    TRUSTED_SUFFIXES = (
        '.cursorvm.com',
        '.agent.cvm.dev',
        'localhost',
        '127.0.0.1',
    )

    def _origin_verified(self, request):
        if settings.DEBUG:
            origin = request.META.get('HTTP_ORIGIN', '')
            referer = request.META.get('HTTP_REFERER', '')
            for value in (origin, referer):
                if value and any(suffix in value for suffix in self.TRUSTED_SUFFIXES):
                    return True
        return super()._origin_verified(request)
