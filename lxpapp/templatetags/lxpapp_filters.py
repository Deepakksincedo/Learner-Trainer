from django import template

register = template.Library()

@register.filter
def sort_by_name(users):
    return sorted(users, key=lambda u: (u.first_name, u.last_name))