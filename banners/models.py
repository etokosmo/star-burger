from pathlib import Path

from django.db import models


def get_upload_path(instance, filename):
    return Path("banner") / filename


class Slug(models.Model):
    slug_title = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Слаг")

    class Meta:
        verbose_name = "Slug"
        verbose_name_plural = "Slugs"

    def __str__(self):
        return self.slug_title


class Banner(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=100,
        db_index=True,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to=get_upload_path
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    slug = models.ForeignKey(
        Slug,
        on_delete=models.CASCADE,
        verbose_name="Слаг",
        related_name="banners",
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        verbose_name='Порядок',
        blank=True,
        default=0
    )

    class Meta:
        ordering = ["-order"]
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self):
        return f"{self.title} - {self.text}"
