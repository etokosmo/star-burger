from pathlib import Path

from django.db import models


def get_upload_path(instance, filename):
    return Path("banner") / filename


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

    def __str__(self):
        return f"{self.title} - {self.text}"
