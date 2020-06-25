import factory
from .models import Category, Product
from user.factories import UserFactory
from django.utils.text import slugify


class CategoryFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Title of category {}'.format(n))
    slug = factory.LazyAttribute(lambda o: slugify(o.title))

    class Meta:
        model = Category


# class StoreFactory(factory.DjangoModelFactory):
#     type = factory.SubFactory(TypeFactory)
#     title = factory.Faker('company')
#     slug = factory.LazyAttribute(lambda o: slugify(o.title))
#     document_number = factory.Sequence(lambda n: '1111111111111{}'.format(n))
#     is_active = factory.Iterator([True, False])
#
#     class Meta:
#         model = Store
#
#     @factory.post_generation
#     def members(self, create, extracted, **kwargs):
#         if not create:
#             # Simple build, do nothing.
#             return
#
#         if extracted:
#             # A list of members were passed in, use them
#             for member in extracted:
#                 self.members.add(member)
#
#
# class MembershipFactory(factory.DjangoModelFactory):
#     user = factory.SubFactory(UserFactory)
#     store = factory.SubFactory(StoreFactory)
#     is_owner = factory.Iterator([True, False])
#     is_staff = factory.Iterator([True, False])
#     is_customer = factory.Iterator([True, False])
#
#     class Meta:
#         model = Membership
#
#
# class StoreWithMembershipsFactory(UserFactory):
#     membership1 = factory.RelatedFactory(MembershipFactory, 'user')
#     membership2 = factory.RelatedFactory(MembershipFactory, 'user')
#
#     class Meta:
#         exclude = ['object']
