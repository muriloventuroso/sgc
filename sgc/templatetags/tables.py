from django.template import Library

register = Library()


@register.filter
def range_paginator(value, current):
    r"""Take a number and iterates and returns a range (list).

    Syntax:
    {% num_range 5 as some_range %}

    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}

    Produces:
    0: Something I want to repeat
    1: Something I want to repeat
    2: Something I want to repeat
    3: Something I want to repeat
    4: Something I want to repeat
    """
    return [i + 1 for i in range(0, value) if i > current - 6 and i < current + 4]


@register.simple_tag
def active_pagination(value, current):
    if int(value) == int(current):
        return 'active'

