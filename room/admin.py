from django.contrib import admin
from room.models import Category, Room


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    list_filter = ('title',)
    search_fields = ('title',)
    ordering = ('title',)
    filter_horizontal = ()
    fieldsets = [
        (None, {'fields': ['title']}),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room)
