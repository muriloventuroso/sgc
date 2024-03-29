# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.utils.encoding import force_str


def text_value(value):
    """
    Force a value to text, render None as an empty string
    """
    if value is None:
        return ""
    return force_str(value)


def text_concat(*args, **kwargs):
    """
    Concatenate several values as a text string with an optional separator
    """
    separator = text_value(kwargs.get("separator", ""))
    values = filter(None, [text_value(v) for v in args])
    return separator.join(values)
