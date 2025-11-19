from django.contrib import admin
from products.models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'is_available', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active', 'created_date')
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active')
    list_editable = ('is_active',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
