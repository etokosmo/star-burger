from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, \
    SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from .models import Banner, Slug


class BannerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Banner
    extra = 0
    readonly_fields = ["get_preview"]

    def get_preview(self, image):
        return format_html(
            "<img src={} style='max-height: 70px;'>",
            image.image.url
        )


@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    raw_id_fields = ("slug",)
    list_display = [
        'title',
        'get_preview',
        'text',
        'slug',
    ]
    list_filter = ("slug",)

    def get_preview(self, image):
        return format_html(
            "<img src={} style='max-height: 70px;'>",
            image.image.url
        )


@admin.register(Slug)
class SlugAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        BannerInline,
    ]
