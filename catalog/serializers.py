from rest_framework import serializers
from .models import Category, Product
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=60, help_text=_('The title of the category.'))
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Category.objects.all())],
        max_length=150,
        required=False,
        allow_blank=False,
        help_text=_('The slug of the category.')
    )

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=60, help_text=_('The title of the product.'))
    description = serializers.CharField(required=True, help_text=_('The description of the product.'))
    slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=Category.objects.all())],
        max_length=150,
        required=False,
        allow_blank=False,
        help_text=_('The slug of the product.')
    )
    categories = CategorySerializer(many=True, read_only=False)

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'description', 'categories')


class ProductWriteSerializer(ProductSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Category.objects.all(),
        many=True,
        read_only=False,
    )
