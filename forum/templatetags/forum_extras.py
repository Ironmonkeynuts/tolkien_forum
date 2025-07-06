from django import template

register = template.Library()


@register.filter
def model_name(instance):
    """Returns the class name of the model instance."""
    return instance.__class__.__name__
