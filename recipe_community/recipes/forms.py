from django import forms
from django.forms import BaseInlineFormSet

from . import models


class CreateUpdateRecipeForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=models.TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    tags.widget.attrs.update({'class': ' tags__checkbox_style_green'})

    class Meta:
        model = models.Recipe
        fields = ['title', 'how_to', 'cooking_time', 'image', 'tags']


class IngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=models.Ingredient.objects.order_by('name')
    )

    class Meta:
        model = models.RecipeIngredient
        fields = ['ingredient', 'amount', 'unit']
        widgets = {
            'ingredient': forms.Select(attrs={'id': 'nameIngredient',
                                              'class': 'form__input'}),
            'amount': forms.NumberInput(attrs={'id': 'cantidad',
                                               'class': 'form__input',
                                               'style': 'max-width: 100px;'}),
            'unit': forms.TextInput(attrs={'id': 'cantidadVal',
                                           'class': 'form__input',
                                           'style': 'max-width: 100px;'})
        }


class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            for field in form.fields:
                field.widget.attrs.update({'class': 'form__input'})


IngredientFormset = forms.inlineformset_factory(
    models.Recipe,
    models.RecipeIngredient,
    form=IngredientForm,
    extra=1,
    can_delete=True
)
