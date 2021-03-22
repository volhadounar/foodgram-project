from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_bookmarked(recipe, user):
    return recipe.favorite_for.filter(id=user.id).exists()


@register.filter
def is_bought(recipe, user):
    return recipe.orders.filter(id=user.id).exists()
