from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class TagInline(admin.TabularInline):
    model = Tag.recipes.through


class IngredientInline(admin.TabularInline):
    model = Ingredient.for_recipes.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_who', 'display_tags_as_str',
                    'display_ingredients', 'display_bookmarked')
    search_fields = ('title',)
    list_filter = ('from_who', 'title', 'tags')
    readonly_fields = ('display_tags_as_str', 'display_ingredients',
                       'display_bookmarked')
    empty_value_display = '-empty-'

    fieldsets = (
        ('Main', {
            'fields': ('title', 'from_who', 'how_to',
                       'cooking_time', 'display_tags_as_str',
                       'display_bookmarked', 'display_ingredients')
        }),
        ('Show photos', {
            'fields': ('image',)
        }),
    )
    inlines = [TagInline, IngredientInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
