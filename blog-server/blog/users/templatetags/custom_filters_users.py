from django import template

register = template.Library()
@register.simple_tag
def get_type(request):
    print(request.session['type'])
    return request.session['type']
