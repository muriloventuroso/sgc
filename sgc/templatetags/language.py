from django import template

register = template.Library()


@register.simple_tag
def url_language(request, value):
    seg = request.path.split('/')
    dict_ = request.GET.copy()
    url = '/' + value + '/' + '/'.join(seg[2:]) + '?' + dict_.urlencode()
    return url
