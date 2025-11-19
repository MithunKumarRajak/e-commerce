from django.db import models
from products.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variation_color = models.ForeignKey(Variation, related_name='cart_items_color', null=True, blank=True, on_delete=models.SET_NULL)
    variation_size = models.ForeignKey(Variation, related_name='cart_items_size', null=True, blank=True, on_delete=models.SET_NULL)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        parts = [self.product.product_name]
        if self.variation_color:
            parts.append(f"Color: {self.variation_color.variation_value}")
        if self.variation_size:
            parts.append(f"Size: {self.variation_size.variation_value}")
        return " - ".join(parts)
