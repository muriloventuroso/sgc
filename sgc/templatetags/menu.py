from django.template import Library

register = Library()


@register.simple_tag
def show_entry(app, value):
    if app == value:
        return 'show'
