from django import template

register = template.Library()


@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1]
    except Exception:
        return ''


@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) - 1]
    except Exception:
        return ''


@register.simple_tag
def list_names(queryset, ids, names=None):
    if names:
        n_names = names
    else:
        data = list(queryset.all())
        names = []
        for id in ids:
            for d in data:
                if str(d._id) == id:
                    names.append(d)
                    break
        n_names = [str(x) for x in names]
    return ', '.join(n_names)
