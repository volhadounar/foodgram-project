from django import forms

import django_filters

from .models import Recipe, Tag


class TagFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'id': 'id_tag',
                   'class': 'tags__checkbox tags__checkbox_style_green'})
    )

    class Meta:
        model = Recipe
        fields = ['tags']
