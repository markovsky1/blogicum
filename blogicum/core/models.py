from django.db import models


# Create your models here.
class CreatedPublishedModel(models.Model):
    """Абстрактная модель. Добавляет created_at и флаг is_published."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
