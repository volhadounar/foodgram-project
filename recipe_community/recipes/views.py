from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from recipe_community.settings import PAGINATION_CNT_ON_PAGE

from .filters import TagFilter
from .forms import CreateUpdateRecipeForm, IngredientFormset
from .models import Bookmark, Follow, Order, Recipe, User
from .owner import OwnerCreateView, OwnerDeleteView, OwnerUpdateView
from .pdf import BuildPdf
from .updater import CreateDeleteOwnedView, CreateDeleteView


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


class ProfileView(ListView):
    template_name = 'recipes/profile.html'
    model = Recipe

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        id = self.kwargs.get('pk', 0)
        user = get_object_or_404(User, id=id)
        return qs.filter(from_who=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        put_filtered_paged_recipe_list(self.request, context)
        user_id = self.kwargs.get('pk', 0)
        owner = get_object_or_404(User, id=user_id)
        context['owner'] = owner
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user).filter(author=owner).exists()
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name_suffix = '_detail_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = context['recipe'].from_who
        if self.request.user.is_authenticated:
            context['following'] = Follow.objects.filter(
                user=self.request.user).filter(author=owner).exists()
        return context


class RecipeCreateView(OwnerCreateView):
    model = Recipe
    form_class = CreateUpdateRecipeForm
    template_name_suffix = '_create_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_formset'] = IngredientFormset(
            self.request.POST or None, self.request.FILES or None
        )
        return context

    def form_valid(self, main_form):
        res = super(RecipeCreateView, self).form_valid(main_form)
        if res.status_code not in [200, 302]:
            return res
        ingredients_formset = self.get_context_data().get(
            'ingredients_formset')
        if ingredients_formset.is_valid():
            instanses = ingredients_formset.save(commit=False)
            for instance in instanses:
                instance.recipe = main_form.instance
                instance.save()
        return res

    def get_success_url(self, **kwargs):
        return reverse('recipes:profile', args=[self.request.user.id])


class RecipeUpdateView(OwnerUpdateView):
    model = Recipe  # {{ recipe }}
    form_class = CreateUpdateRecipeForm
    template_name_suffix = '_create_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = context.get('recipe')
        context['ingredients_formset'] = IngredientFormset(
            self.request.POST or None, self.request.FILES or None,
            instance=recipe
        )
        return context

    def form_valid(self, main_form):
        res = super(UpdateView, self).form_valid(main_form)
        if res.status_code not in [200, 302]:
            return res

        ingredients_formset = self.get_context_data().get(
            'ingredients_formset')
        if ingredients_formset.is_valid():
            ingredients_formset.save()
        return res

    def get_success_url(self, **kwargs):
        return reverse('recipes:profile', args=[self.request.user.id])


class RecipeDeleteView(OwnerDeleteView):
    model = Recipe
    template_name_suffix = '_delete_form'

    def get_success_url(self, **kwargs):
        return reverse('recipes:profile', args=[self.request.user.id])


class RecipeAllView(ListView):
    model = Recipe  # {{ recipe_list }}
    template_name = 'recipes/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        put_filtered_paged_recipe_list(self.request, context)
        return context


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'recipes/subscriptions_list.html'
    more_for = {}

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(
            following__user=self.request.user).order_by('username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = context.get('user_list', [])
        paginator = Paginator(user_list, PAGINATION_CNT_ON_PAGE)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        for user in paginator.get_page(page_number):
            if user.username not in self.more_for:
                self.more_for[user.username] = 2
        for key in dict(self.request.GET).keys():
            if key.startswith('morefor_'):
                user = key.split('_')[1]
                self.more_for[user] += 1
        context['more'] = self.more_for
        return context


class BookmarkChangeView(CreateDeleteOwnedView):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        Bookmark.objects.get_or_create(user=self.request.user, recipe=recipe)
        return redirect(reverse_lazy('recipes:bookmarks'))

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        Bookmark.objects.filter(user=self.request.user,
                                recipe=recipe).delete()
        return redirect(reverse_lazy('recipes:bookmarks'))


class BookmarksListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/bookmarks_list.html'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.favorite_recipes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        put_filtered_paged_recipe_list(self.request, context)
        return context


class OrderListView(ListView):
    model = Recipe
    template_name = 'recipes/order_list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.request.user.ordered_recipes.all()
        ordered_ids = self.request.session.get('ordered_recipes', [])
        recipe_list = Recipe.objects.filter(id__in=ordered_ids)
        return recipe_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        put_filtered_paged_recipe_list(self.request, context)
        return context


class FollowChangeView(CreateDeleteOwnedView):
    def post(self, *args, **kwargs):
        username = kwargs.get('username', '')
        if self.request.user.get_username() == username:
            return redirect(reverse('recipes:profile',
                                    args=[self.request.user.id]))
        author = get_object_or_404(User, username=username)
        Follow.objects.get_or_create(user=self.request.user, author=author)
        return redirect(reverse('recipes:profile',
                                args=[self.request.user.id]))

    def delete(self, *args, **kwargs):
        username = kwargs.get('username', '')
        if self.request.user.get_username() == username:
            return redirect(reverse('recipes:index'))
        author = get_object_or_404(User, username=username)
        Follow.objects.filter(user=self.request.user, author=author).delete()
        return redirect(reverse('recipes:profile',
                                args=[self.request.user.id]))


class OrderChangeView(CreateDeleteView):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.user.is_authenticated:
            Order.objects.get_or_create(user=self.request.user, recipe=recipe)
        else:
            if 'ordered_recipes' not in self.request.session:
                self.request.session['ordered_recipes'] = []
            recipe_list_ids = self.request.session['ordered_recipes']
            if pk not in recipe_list_ids:
                recipe_list_ids.append(pk)
            self.request.session['ordered_recipes'] = recipe_list_ids
        return redirect(reverse_lazy('recipes:order_list'))

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        if self.request.user.is_authenticated:
            Order.objects.filter(user=self.request.user,
                                 recipe=recipe).delete()
        elif 'ordered_recipes' not in self.request.session:
            return redirect(reverse_lazy('recipes:order_list'))
        recipe_list_ids = self.request.session['ordered_recipes']
        index = recipe_list_ids.index(pk)
        del recipe_list_ids[index]
        self.request.session['ordered_recipes'] = recipe_list_ids
        return redirect(reverse_lazy('recipes:order_list'))


def orders_view(request):
    if request.user.is_authenticated:
        query = request.user.ordered_recipes.all()
    else:
        ordered_ids = request.session.get('ordered_recipes', [])
        query = Recipe.objects.filter(id__in=ordered_ids)
    res = {}
    for recipe in query:
        for item in recipe.recipeingredient_set.all():
            if item not in res:
                res[item.ingredient.name] = [item.amount, item.unit]
            else:
                res[item.ingredient.name][0] += item.amount

    buffer = BuildPdf(res, request.user)
    return FileResponse(buffer, as_attachment=True,
                        filename='shoppinglist.pdf')


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
