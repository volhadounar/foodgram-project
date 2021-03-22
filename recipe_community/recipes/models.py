from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Name', max_length=64,
        help_text='Please enter an ingredient name of max 64 characters.',
        unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(
        'Recipe name', max_length=64,
        help_text='Please give a short name to the recipe.', null=False)
    # slug = models.SlugField(
    #                 'Slug', max_length=64,
    #                 help_text='Please specify an address for the task page. \
    #                 Use only Latin, numbers, hyphens and underscores.',
    #                 unique=True)
    from_who = models.ForeignKey(User, related_name='recipes',
                                 verbose_name='From',
                                 db_index=True, on_delete=models.CASCADE,
                                 help_text='This recipe from.', null=False)
    how_to = models.TextField('How to', max_length=1024,
                              help_text='How to make.', null=False)
    cooking_time = models.IntegerField(
        'Cooking time',
        help_text='Please enter a cooking time in minutes.',
        null=True
    )
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ingredients',
                                         through='Recipe_Ingredient',
                                         related_name='for_recipes')
    tags = models.ManyToManyField('Tag', through='Recipe_Tag',
                                  verbose_name='Tags')
    favorite_for = models.ManyToManyField(User, through='Bookmarks',
                                          related_name='favorite_recipes')
    orders = models.ManyToManyField(User, through='Order',
                                    related_name='orders')
    image = models.ImageField('Illustration', upload_to='image/', blank=True,
                              null=True,
                              help_text='Upload image.')
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)

    def get_absolute_url(self):
        return '/%s/' % self.id

    def display_tags_as_str(self):
        """Create a string for the Tag.
           This is required to display tags in Admin."""
        return ', '.join(str(tag.name) for tag in self.tags.all())

    def display_tags_as_list(self):
        """Create a list for the Tag.
           This is required to display tags in Recipe's page."""
        return [tag.name for tag in self.tags.all()]

    def display_ingredients_as_list(self):
        """Create a list for the Ingredients set.
           This is required to display ingredients in Recipe's page."""
        return [(i.ingredient.name, i.amount, i.unit)
                for i in self.recipe_ingredient_set.all()]

    def display_ingredients_as_str(self):
        """Create a string for the Ingredients set.
           This is required to display ingredients in Recipe's page."""
        return ', '.join(i.name for i in self.ingredients.all())

    def display_ingredients(self):
        """Create a string for the Ingredient.
           This is required to display tags in Admin."""
        return '; '.join(i.ingredient.name + ','
                         + str(i.amount) + ''
                         + (str(i.unit) if i.unit else '')
                         for i in self.ingredients.through.objects.all()
                         )

    def display_bookmarked(self):
        """Create a string for the favorite_for field.
           This is required to display tags in Admin."""
        return str(self.favorite_for.all().count()) + ' times'

    display_tags_as_str.short_description = 'tags'
    display_tags_as_list.short_description = 'list_of_tags'
    display_ingredients.short_description = 'ingredients'
    display_bookmarked.short_description = 'bookmarked'

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class Recipe_Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True)
    unit = models.CharField('Measurement units', max_length=32, default='g',
                            null=True, blank=True)

    def __str__(self):
        return "Recipe " + str(self.recipe.title) + " <--> ingredient " \
            + str(self.ingredient.name)


class Tag(models.Model):
    TAG_CHOICES = (
        ('vegetarian', 'vegetarian'),
        ('macrobiotic diet', 'macrobiotic diet'),
        ('mediterrenean diet', 'mediterrenean diet'),
        ('vegan diet', 'vegan diet'),
        ('raw food', 'raw food'),
        ('old recipes', 'old recipes'),
        ('fastfood', 'fastfood'),
        ('baking', 'baking'),
        ('gluten free', 'gluten free')
    )
    name = models.CharField(
        'Name',
        help_text='Please select a name from the available.',
        choices=TAG_CHOICES, default='macrobiotic diet',
        unique=True, max_length=20)
    recipes = models.ManyToManyField('Recipe', through='Recipe_Tag')

    def __str__(self):
        return str(self.name)


class Recipe_Tag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag', 'recipe'],
                                    name='unique_recipe_tag'),
        ]

    def __str__(self):
        return "Tag " + str(self.tag.name) + " <--> recipe " + \
               str(self.recipe.title)


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_bookmarks'),
        ]

    def __str__(self):
        return "User " + str(self.user.id) + " <--> recipe " + \
               str(self.recipe.id)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_order'),
        ]

    def __str__(self):
        return "User " + str(self.user.id) + " <--> recipe " + \
               str(self.recipe.id)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
        ]
