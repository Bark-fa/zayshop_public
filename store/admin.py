from django.contrib import admin

from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'list_date')
    list_display_links = ('id', 'name')
    list_filter = ('list_date', 'price')
    search_fields = ('name', 'description', 'price')
    list_per_page = 25


admin.site.register(Product, ProductAdmin)
