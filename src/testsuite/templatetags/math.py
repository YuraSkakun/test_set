from django import template

register = template.Library()


def mult(value, arg):
    return value * arg


@register.filter(name='div')
def div(value, arg):
    return value / arg


@register.simple_tag(name='expr')
def expr(value, *args):
    # value = "(%1 + %2) * %3"  ----if  args = (4, 5, 6) ==> (4 + 5) * 6 or if:
    # value = "(%1 + %3) * %2"  ----if  args = (4, 5, 6) ==> (4 + 6) * 5
    # for idx, arg in enumerate(args)  --- start with 0
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
        # value.replace('%1', str(4)) ==> '(4 + %3) * %2'
    return eval(value)


register.filter('mult', mult)
