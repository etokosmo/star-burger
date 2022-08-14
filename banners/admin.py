from django.contrib import admin

from .models import Banner, Slug


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    raw_id_fields = ("slug",)


@admin.register(Slug)
class SlugAdmin(admin.ModelAdmin):
    pass
