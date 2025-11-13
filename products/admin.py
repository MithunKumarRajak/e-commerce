from django.contrib import admin
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'is_available', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


# Register your models here.
admin.site.register(Product, ProductAdmin)
