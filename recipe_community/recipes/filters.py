from django import forms
from django.db.models import Q

import django_filters

from .models import Recipe, TAG_CHOICES


class TagFilter(django_filters.FilterSet):
    tags = django_filters.MultipleChoiceFilter(
        choices=TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'id_tag',
                   'class': 'tags__checkbox tags__checkbox_style_green'}),
        method='filter_interests'
    )

    def filter_interests(self, queryset, name, flt_tags):
        search_params = Q()
        for tag in flt_tags:
            search_params = search_params | Q(tags__contains=tag)
        return queryset.filter(search_params)

    class Meta:
        model = Recipe
        fields = ['tags']
