from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(from_who=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(from_who=self.request.user)


class OwnerCreateView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        object = form.save(commit=False)
        object.from_who = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)


class OwnerListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = super(OwnerListView, self).get_queryset()
        return qs.filter(from_who=self.request.user)
