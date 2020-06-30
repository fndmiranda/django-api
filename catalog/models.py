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
