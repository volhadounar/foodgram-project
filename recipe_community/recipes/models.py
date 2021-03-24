from django.contrib.auth import get_user_model
from django.db import models

from multiselectfield import MultiSelectField

User = get_user_model()

vegetarian = 100
macrobiotic = 150
mediterrenean = 160
vegan = 170
raw = 180
old = 190
fastfood = 200
baking = 210
glutfree = 220

TAG_CHOICES = (
    (vegetarian, 'vegetarian'),
    (macrobiotic, 'macrobiotic diet'),
    (mediterrenean, 'mediterrenean diet'),
    (vegan, 'vegan diet'),
    (raw, 'raw food'),
    (old, 'old recipes'),
    (fastfood, 'fastfood'),
    (baking, 'baking'),
    (glutfree, 'gluten free')
)


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Name', max_length=64,
        help_text='Please enter an ingredient name of max 64 characters.',
        unique=True)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Recipe name', max_length=64,
        help_text='Please give a short name to the recipe.')
    from_who = models.ForeignKey(User, related_name='recipes',
                                 verbose_name='From',
                                 db_index=True, on_delete=models.CASCADE,
                                 help_text='This recipe from.',)
    how_to = models.TextField(verbose_name='How to', max_length=1024,
                              help_text='How to make.')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Cooking time',
        help_text='Please enter a cooking time in minutes.',
        null=True
    )
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ingredients',
                                         through='RecipeIngredient',
                                         related_name='for_recipes')
    favorite_for = models.ManyToManyField(User, through='Bookmark',
                                          related_name='favorite_recipes')
    orders = models.ManyToManyField(User, through='Order',
                                    related_name='ordered_recipes')
    image = models.ImageField(verbose_name='Illustration', upload_to='image/',
                              blank=True,
                              null=True,
                              help_text='Upload image.')
    pub_date = models.DateTimeField(verbose_name='Date of publication',
                                    auto_now_add=True)
    tags = MultiSelectField(verbose_name='Tags', choices=TAG_CHOICES)

    def display_tags_as_list(self):
        """Create a list for the Tag.
           This is required to display tags in Recipe's page."""
        return str(self.tags).split(',')

    def display_ingredients_as_list(self):
        """Create a list for the Ingredients set.
           This is required to display ingredients in Recipe's page."""
        query_set = self.recipeingredient_set.values_list(
            'ingredient__name', 'amount', 'unit'
        )
        return [(name, amount, unit) for name, amount, unit in query_set]

    def display_ingredients_as_str(self):
        """Create a string for the Ingredients set.
           This is required to display ingredients in Recipe's page."""
        return ', '.join(
            name for name in self.ingredients.values_list('name', flat=True)
        )

    def display_ingredients(self):
        """Create a string for the Ingredient.
           This is required to display tags in Admin."""
        return '; '.join(
            name + ',' + str(amount) + unit
            for name, amount, unit
            in self.ingredients.through.objects.values_list(
                'ingredient__name', 'amount', 'unit')
        )

    def display_bookmarked(self):
        """Create a string for the favorite_for field.
           This is required to display tags in Admin."""
        return str(self.favorite_for.all().count()) + ' times'

    display_tags_as_list.short_description = 'list_of_tags'
    display_ingredients.short_description = 'ingredients'
    display_bookmarked.short_description = 'bookmarked'

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.id


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    unit = models.CharField(verbose_name='Measurement units',
                            max_length=32, default='g',
                            null=True, blank=True)

    class Meta:
        verbose_name = 'RecipeAndIngredinents'
        verbose_name_plural = 'RecipeAndIngredinents'

    def __str__(self):
        return ("Recipe " + str(self.recipe.title) + " <--> ingredient "
                + str(self.ingredient.name))


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_bookmarks'),
        ]
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return ("User " + str(self.user.id) + " <--> recipe "
                + str(self.recipe.id))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_order'),
        ]
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return ("User " + str(self.user.id) + " <--> recipe "
                + str(self.recipe.id))


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
        ]
        verbose_name = 'Follow'
        verbose_name_plural = 'Follow'
