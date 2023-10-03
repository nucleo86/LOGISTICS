from django import template
import hashlib

register = template.Library()

@register.filter
def generate_color(employee):
    if not employee or not employee.first_name or not employee.last_name:
        return "rgba(255, 255, 255, 1)"

    full_name = employee.first_name + ' ' + employee.last_name
    hash_value = abs(hash(full_name))
    r = (hash_value & 0xFF0000) >> 16
    g = (hash_value & 0x00FF00) >> 8
    b = hash_value & 0x0000FF

    color = "rgba({},{},{},0.4)".format(r, g, b)

    return color
