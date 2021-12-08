from django.db.models import fields
import django_filters
from django_filters.filters import CharFilter
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    skill__name = CharFilter(field_name='skill__name', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'skill__name']
