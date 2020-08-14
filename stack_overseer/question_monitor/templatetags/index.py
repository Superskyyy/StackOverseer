"""
It's not possible to access list index during django template without this tag.
"""
from django import template

register = template.Library()


# We really need this new tag to access list index..
@register.filter
def index(sequence, position):
    return sequence[position]
