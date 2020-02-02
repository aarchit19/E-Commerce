from django import template
register=template.Library()
def getvalue(value,arg):
    return value[arg]

register.filter('getvalue',getvalue)
