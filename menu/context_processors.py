from .utils import get_ingress_token


from .utils import get_ingress_token


def ingress_token(request):
    """إتاحة توكن البروكسي في القوالب"""
    return {'ingress_token': get_ingress_token(request)}
