from django.template import Library
register = Library()
@register.filter('multipy')
def multipy(a,b):
    return int(a)*int(b)