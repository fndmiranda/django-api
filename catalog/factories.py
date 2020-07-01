import factory
from .models import Category, Product
from django.utils.text import slugify


class CategoryFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Title of category {}'.format(n))
    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = Category


class ProductFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Title of product {}'.format(n))
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    is_active = factory.Faker('pybool')
    ordering = factory.Faker('pyint', min_value=1, max_value=50)
    brand = factory.Faker('company')
    description = factory.Faker('sentence')

    class Meta:
        model = Product
