from django import template
from django.core.exceptions import ObjectDoesNotExist

from goals.models import Copy

register = template.Library()

def static_copy(name):
    try:
        copy = Copy.objects.get(name=name)
        result = copy.content
    except ObjectDoesNotExist:
        result = None
    return result
register.simple_tag(static_copy)

