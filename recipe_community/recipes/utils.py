from django.core.paginator import Paginator

from recipe_community.settings import PAGINATION_CNT_ON_PAGE

from .filters import TagFilter


def put_filtered_paged_recipe_list(request, context: dict):
    recipe_list = context.get('recipe_list', [])
    if len(recipe_list) == 0:
        return
    flt = TagFilter(request.GET,
                    queryset=recipe_list)
    if len(request.GET.get('tags', [])):
        paginator = Paginator(flt.qs, PAGINATION_CNT_ON_PAGE)
    else:
        paginator = Paginator(recipe_list, PAGINATION_CNT_ON_PAGE)
    page_number = request.GET.get('page')
    context['page'] = paginator.get_page(page_number)
    context['tag_filter'] = flt
