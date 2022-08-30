from django import template

register = template.Library()


@register.simple_tag
def underscoreTag(obj, attribute):
    obj = dict(obj)
    return obj.get(attribute)
