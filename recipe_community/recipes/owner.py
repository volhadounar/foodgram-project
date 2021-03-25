from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin


class OwnerSingleObjectMixin(SingleObjectMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(from_who=self.request.user)


class OwnerListView(LoginRequiredMixin, OwnerSingleObjectMixin, ListView):
    pass


class OwnerUpdateView(LoginRequiredMixin, OwnerSingleObjectMixin, UpdateView):
    pass


class OwnerDeleteView(LoginRequiredMixin, OwnerSingleObjectMixin, DeleteView):
    pass


class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        object = form.save(commit=False)
        object.from_who = self.request.user
        object.save()
        return super().form_valid(form)
