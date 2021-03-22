from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class CreateDeleteView(LoginRequiredMixin, View):
    http_method_names = ['post', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'post':
            return self.post(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CreateDeleteView, self).dispatch(*args, **kwargs)
