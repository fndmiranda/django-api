from django.db import models
from base.helpers import generate_unique_slug
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('title'))
    slug = models.SlugField(blank=False, max_length=80, verbose_name=_('slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def save(self, *args, **kwargs):
        if self.pk is None:  # create
            if not self.slug:
                self.slug = generate_unique_slug(Category, self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=64, verbose_name=_('title'))
    slug = models.SlugField(max_length=80, verbose_name=_('slug'))
    categories = models.ManyToManyField(Category, related_name='products', blank=True, verbose_name=_('categories'))
    description = models.TextField(verbose_name=_('description'))
    brand = models.CharField(max_length=50, verbose_name=_('brand'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    ordering = models.IntegerField(default=0, db_index=True, verbose_name=_('ordering'))
    released_at = models.DateTimeField(null=True, verbose_name=_('released at'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def save(self, *args, **kwargs):
        if self.pk is None:  # create
            if not self.slug:
                self.slug = generate_unique_slug(Product, self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('ordering',)

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    product = models.ForeignKey(Product, related_name='models', on_delete=models.CASCADE, verbose_name=_('product'))
    title = models.CharField(max_length=64, verbose_name=_('title'))
    slug = models.SlugField(blank=False, max_length=80, verbose_name=_('slug'))
    description = models.TextField(verbose_name=_('description'))
    sku = models.CharField(blank=False, max_length=32, verbose_name=_('sku'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    pre_sale = models.BooleanField(default=False, verbose_name=_('pre sale'))
    weight = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_('weight'))  # in KG
    height = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_('height'))  # in meters
    width = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_('width'))  # in meters
    depth = models.DecimalField(max_digits=8, decimal_places=3, verbose_name=_('depth'))  # in meters
    ordering = models.IntegerField(default=0, db_index=True, verbose_name=_('ordering'))
    released_at = models.DateTimeField(null=True, verbose_name=_('released at'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def save(self, *args, **kwargs):
        if self.pk is None:  # create
            self.slug = generate_unique_slug(ProductModel, self.slug if self.slug else self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('model')
        verbose_name_plural = _('models')
        ordering = ('ordering',)

    def __str__(self):
        return self.title
