from django import template
from django.core.exceptions import ObjectDoesNotExist

from django-goaltracking.goals.models import Quote

register = template.Library()

def daily_quote(w,d):
    try:
        quote = Quote.objects.get(week=w,day=d)
    except ObjectDoesNotExist:
        quote = None
    return quote
register.simple_tag(daily_quote)

