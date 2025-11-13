from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    # Slug field for URL-friendly representation
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    category_image = models.ImageField(
        upload_to='categories/', blank=True, null=True)



    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
