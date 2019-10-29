from django import template
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

register = template.Library()


@register.filter
def currency(num):
    return locale.currency(num, grouping=True, symbol='R$')
