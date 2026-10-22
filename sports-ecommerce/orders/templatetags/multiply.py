from django import template
register=template.Library()
@register.simple_tag(name="multiply")
def multiply(a,b):
    try:
        return float(a)*int(b)
    except (ValueError,TypeError):
        return 0