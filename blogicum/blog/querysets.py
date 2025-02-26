from django.db import models
from django.db.models import Count
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def published(self):
        current_time = timezone.now()
        return self.filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        )

    def comment_count(self):
        return self.annotate(
            comment_count=Count('comments')
        )
