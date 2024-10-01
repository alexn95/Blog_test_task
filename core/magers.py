from django.db.models import Count
from django.db.models import Manager


class PostManager(Manager):

    def queryset(self):
        return self.prefetch_related('comments', 'tags')

    def with_comments_count(self):
        return self.queryset().annotate(comments_count=Count('comments', distinct=True))
