from django import template


def flip(value):
    if value:
        adjusted_value = False
    elif value is False:
        adjusted_value = True
    else:
        adjusted_value = False
        
    return adjusted_value


register = template.Library()

register.filter('flip', flip)
