from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at',)
    list_filter = ('title',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title', 'slug']}),
    ]


admin.site.register(Category, CategoryAdmin)
