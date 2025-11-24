from django.contrib import admin
import admin_thumbnails
from products.models import Product, ProductGallery, Variation, ReviewRating


# ---------------------------------------------------------
# PREDEFINED VARIATION VALUES (no typing needed)
# ---------------------------------------------------------
COLOR_VALUES = ["Black", "Blue", "Red",
                "White", "Silver", "Gold", "Brown", "Grey"]
SIZE_VALUES = ["S", "M", "L", "XL", "Small", "Medium", "Large"]


# ---------------------------------------------------------
# AUTO-CREATE DEFAULT VARIATIONS (Admin Action)
# ---------------------------------------------------------
@admin.action(description="Generate Default Variations (Size + Color)")
def create_default_variations(modeladmin, request, queryset):
    """
    Creates variations automatically:
    - Size: S, M, L, XL
    - Color: Black, Blue, Red, White
    """
    for product in queryset:
        # Create size variations
        for size in ["S", "M", "L", "XL"]:
            Variation.objects.get_or_create(
                product=product,
                variation_category="size",
                variation_value=size,
                defaults={"is_active": True}
            )
        # Create color variations
        for color in ["Black", "Blue", "Red", "White"]:
            Variation.objects.get_or_create(
                product=product,
                variation_category="color",
                variation_value=color,
                defaults={"is_active": True}
            )


# ---------------------------------------------------------
# PRODUCT GALLERY INLINE
# ---------------------------------------------------------
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


# ---------------------------------------------------------
# VARIATION INLINE
# ---------------------------------------------------------
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    fields = ('variation_category', 'variation_value', 'is_active')
    show_change_link = True


# ---------------------------------------------------------
# PRODUCT ADMIN (MAIN PAGE)
# ---------------------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock',
                    'is_available', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}

    # 👈 ONE CLICK → auto-generate variations
    actions = [create_default_variations]

    # 👈 Inline variations + images
    inlines = [VariationInline, ProductGalleryInline]


# ---------------------------------------------------------
# VARIATION ADMIN (ADVANCED FILTER VIEW)
# ---------------------------------------------------------
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category',
                    'variation_value', 'is_active', 'created_date')
    list_filter = ('product', 'variation_category',
                   'variation_value', 'is_active')
    list_editable = ('is_active',)

    # Optional: Restrict variation_value choices based on category
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "variation_category":
            kwargs['choices'] = [('color', 'Color'), ('size', 'Size')]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    # Predefined dropdown values
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'variation_value':
            formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

            if 'color' in request.path:
                formfield.widget.attrs['placeholder'] = "Enter color"
            formfield.widget.attrs['placeholder'] = "Enter Variation Value (Color / Size)"
            return formfield

        return super().formfield_for_dbfield(db_field, request, **kwargs)


# ---------------------------------------------------------
# REGISTER MODELS
# ---------------------------------------------------------
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
