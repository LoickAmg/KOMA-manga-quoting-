from django.contrib import admin

from .models import Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("character", "series", "theme", "source")
    list_filter = ("series", "theme")
    search_fields = ("character", "series", "text")
