from django import template

register = template.Library()


@register.simple_tag
def dashboard_url(auth_token='', ingress_token='', **params):
    """بناء رابط لوحة التحكم مع التوكنات"""
    parts = [f'{k}={v}' for k, v in params.items()]
    if auth_token:
        parts.append(f'auth_token={auth_token}')
    if ingress_token:
        parts.append(f'_ingress_token={ingress_token}')
    return '?' + '&'.join(parts) if parts else ''
