import datetime

from recipes.models import Recipe, Tag, Ingredient

from django.contrib.auth import get_user_model

from django.test import TestCase


User = get_user_model()


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Paqui', password='111',
                                       email='paqui@punto.es')
        cls.recipe = Recipe.objects.create(
            title='Gluten free bread',
            how_to='Preheat oven to 180°C.Place basmati rice, brown rice, \
                    millet and chickpeas into mixing bowl and mill 1 min/ \
                    speed 9, or until acook flour consistency is achieved...',
            cooking_time=30,
            from_who=cls.user
        )

    def test_recipe_labels(self):
        """Verbose_name field matches expected."""
        recipe = RecipeModelTest.recipe
        field_verboses = {
            'title': 'Recipe name',
            'how_to': 'How to',
            'cooking_time': 'Cooking time',
            'from_who': 'From',
            'ingredients': 'Ingredients',
            'tags': 'Tags',
            'image':'Illustration'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    recipe._meta.get_field(value).verbose_name, expected)

    def test_recipe_help_texts(self):
        """Help_text  field matches expected."""
        recipe = RecipeModelTest.recipe
        field_help_texts = {
            'title': 'Please give a short name to the recipe.',
            'how_to': 'How to make.',
            'cooking_time': 'Please enter a cooking time in minutes.',
            'from_who': 'This recipe from.',
            'image': 'Upload image.'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    recipe._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_field(self):
        """__str__  recipe - is the string with the content of recipe.title"""
        recipe = RecipeModelTest.recipe
        expected_object_name = recipe.title
        self.assertEquals(expected_object_name, str(recipe))


class IngredientModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredient = Ingredient.objects.create(name='basmati rice')

    def test_ingredient_labels(self):
        ingredient = IngredientModelTest.ingredient
        verbose = ingredient._meta.get_field('name').verbose_name
        self.assertEquals(verbose, 'Name')

    def test_ingredient_help_text(self):
        ingredient = IngredientModelTest.ingredient
        help_text = ingredient._meta.get_field('name').help_text
        self.assertEquals(help_text, 'Please enter an ingredient name of max 64 characters.')

    def test_object_name_is_title_field(self):
        """__str__  ingredient - is the string
           with the content of ingredient.name"""
        ingredient = IngredientModelTest.ingredient
        expected_object_name = ingredient.name
        self.assertEquals(expected_object_name, str(ingredient))


class TagModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create()

    def test_tag_labels(self):
        tag = TagModelTest.tag
        verbose = tag._meta.get_field('name').verbose_name
        self.assertEquals(verbose, 'Name')

    def test_tag_help_text(self):
        tag = TagModelTest.tag
        help_text = tag._meta.get_field('name').help_text
        self.assertEquals(help_text, 'Please select a name from the available.')

    def test_object_name_is_name_field(self):
        """__str__  tag - is the string with the content of tag.name"""
        tag = TagModelTest.tag
        expected_object_name = tag.name
        self.assertEquals(str(expected_object_name), str(tag))
