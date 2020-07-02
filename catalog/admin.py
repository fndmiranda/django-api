from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at',)
    list_filter = ('title',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title', 'slug']}),
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'ordering',)
    list_filter = ('title',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'brand', 'ordering', 'is_active']}),
        (None, {'fields': ['description', 'categories']}),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
