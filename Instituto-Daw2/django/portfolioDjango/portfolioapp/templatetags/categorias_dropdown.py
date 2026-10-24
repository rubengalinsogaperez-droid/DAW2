from django import template
from ..models import Categoria
register = template.Library()


@register.inclusion_tag('portfolio/categorias_dropdown.html')
def categorias_dropdown():
    categorias = Categoria.objects.filter()
    return {'categorias': categorias}
