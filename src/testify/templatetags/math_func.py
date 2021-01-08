from django import template

register = template.Library()


@register.simple_tag(name='expr')
def expr(value, *args):
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
    return eval(value)
