from django.contrib import admin
from matter.models import Category, Matter


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('title',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title', 'slug']}),
    ]


class MatterAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category',)
    list_filter = ('title', 'category',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'category']}),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Matter, MatterAdmin)
