import django_filters
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now

from core.models import Post


class PostsFilterSet(django_filters.FilterSet):
    only_last_month = django_filters.BooleanFilter(method='only_last_month_filter')
    author_id = django_filters.NumberFilter(field_name='author__id')
    likes_gt = django_filters.NumberFilter(field_name='likes', lookup_expr='gt')
    tag = django_filters.NumberFilter(field_name='tags__id', lookup_expr='contains')

    def only_last_month_filter(self, queryset, name, value):
        return queryset.filter(published_at__gte=now() - relativedelta(months=1))

    class Meta:
        model = Post
        fields = ('author_id', 'only_last_month', 'likes_gt', 'tag')