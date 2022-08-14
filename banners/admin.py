from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, Slug


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    raw_id_fields = ("slug",)
    list_display = [
        'title',
        'get_preview',
        'text',
        'slug',
    ]

    def get_preview(self, image):
        return format_html(
            "<img src={} style='max-height: 70px;'>",
            image.image.url
        )


@admin.register(Slug)
class SlugAdmin(admin.ModelAdmin):
    pass
