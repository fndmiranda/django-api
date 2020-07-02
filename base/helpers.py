from django.utils.text import slugify


def generate_unique_slug(model, value):
    """
    Generate unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `model` is a class model.
    :param `value` is specific value for slugify.
    """
    origin = slugify(value)
    unique = origin
    numb = 1
    while model.objects.filter(slug=unique).exists():
        unique = '%s-%d' % (origin, numb)
        numb += 1
    return unique
