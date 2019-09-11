from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CategoryManager(models.Manager):
    pass


class MatterManager(models.Manager):
    pass


class Category(models.Model):
    title = models.CharField(max_length=120, verbose_name=_('title'))
    slug = models.SlugField(unique=True, blank=True, max_length=150, verbose_name=_('slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        num = 1
        while Category.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(slug, num)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Matter(models.Model):
    title = models.CharField(max_length=120, verbose_name=_('title'))
    slug = models.SlugField(unique=True, blank=True, max_length=150, verbose_name=_('slug'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))

    objects = MatterManager()

    class Meta:
        verbose_name = _('matter')
        verbose_name_plural = _('matters')

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        num = 1
        while Category.objects.filter(slug=slug).exists():
            slug = '{}-{}'.format(slug, num)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
