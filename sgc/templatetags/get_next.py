from django import template
register = template.Library()

@register.simple_tag
def get_next(request):
    return request.GET.copy().urlencode()
