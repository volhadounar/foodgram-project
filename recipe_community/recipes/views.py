from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from .filters import TagFilter
from .forms import CreateUpdateRecipeForm, IngredientFormset
from .models import Bookmarks, Follow, Order, Recipe, User
from .owner import OwnerCreateView, OwnerDeleteView, OwnerUpdateView
from .pdf import BuildPdf
from .updater import CreateDeleteView


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
        recipe_list = context.get('recipe_list', None)
        flt = TagFilter(self.request.GET,
                        queryset=recipe_list)  # + without queryset
        if len(self.request.GET.get('tags', [])):
            paginator = Paginator(flt.qs, 9)
        else:
            paginator = Paginator(recipe_list, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['tag_filter'] = flt
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
        if self.request.method == 'POST':
            context['ingredients_formset'] = IngredientFormset(
                self.request.POST, self.request.FILES or None
            )
        else:
            context['ingredients_formset'] = IngredientFormset()
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
        recipe = context.get('recipe', None)
        if self.request.method == 'POST':
            context['ingredients_formset'] = IngredientFormset(
                self.request.POST, self.request.FILES or None, instance=recipe
            )
        else:
            context['ingredients_formset'] = IngredientFormset(instance=recipe)
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
        recipe_list = context.get('recipe_list', None)
        flt = TagFilter(self.request.GET,
                        queryset=recipe_list)  # + without queryset
        if len(self.request.GET.get('tags', [])):
            paginator = Paginator(flt.qs, 9)
        else:
            paginator = Paginator(recipe_list, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['tag_filter'] = flt
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
        user_list = context.get('user_list', None)
        paginator = Paginator(user_list, 9)
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


class BookmarkChangeView(CreateDeleteView):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        Bookmarks.objects.get_or_create(user=self.request.user, recipe=recipe)
        return redirect(reverse_lazy('recipes:bookmarks'))

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        Bookmarks.objects.filter(user=self.request.user,
                                 recipe=recipe).delete()
        return redirect(reverse_lazy('recipes:bookmarks'))


class BookmarksListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/bookmarks_list.html'

    def get_queryset(self, *args, **kwargs):
        iam = get_object_or_404(User, id=self.request.user.id)
        return iam.favorite_recipes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_list = context.get('recipe_list', None)
        flt = TagFilter(self.request.GET, queryset=recipe_list)
        if len(self.request.GET.get('tags', [])):
            paginator = Paginator(flt.qs, 9)
        else:
            paginator = Paginator(recipe_list, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['tag_filter'] = flt
        return context


class OrderListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/order_list.html'

    def get_queryset(self, *args, **kwargs):
        iam = get_object_or_404(User, id=self.request.user.id)
        return iam.orders.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_list = context.get('recipe_list', None)
        flt = TagFilter(self.request.GET, queryset=recipe_list)
        if len(self.request.GET.get('tags', [])):
            paginator = Paginator(flt.qs, 9)
        else:
            paginator = Paginator(recipe_list, 9)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)
        context['tag_filter'] = flt
        return context


class FollowChangeView(CreateDeleteView):
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
        Order.objects.get_or_create(user=self.request.user, recipe=recipe)
        return redirect(reverse_lazy('recipes:order_list'))

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        recipe = get_object_or_404(Recipe, id=pk)
        Order.objects.filter(user=self.request.user, recipe=recipe).delete()
        return redirect(reverse_lazy('recipes:order_list'))


@login_required
def orders_view(request):
    res = {}
    for item in request.user.orders.all():
        for i in item.recipe_ingredient_set.all():
            if i not in res:
                res[i.ingredient.name] = [i.amount, i.unit]
            else:
                res[i.ingredient.name][0] += i.amount

    buffer = BuildPdf(res, request.user)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
