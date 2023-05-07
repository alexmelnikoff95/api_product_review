from django_filters import rest_framework as rf
from .models import Product


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(rf.BaseInFilter, rf.CharFilter):
    pass


class ProductFilter(rf.FilterSet):
    country = CharFilterInFilter(field_name='country', lookup_expr='in')
    year = rf.RangeFilter()

    class Meta:
        model = Product
        fields = ['year']
