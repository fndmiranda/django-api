from django.db import models
from django.conf import settings


class CategoryManager(models.Manager):
    pass


class Category(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "categories"


class Room(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
