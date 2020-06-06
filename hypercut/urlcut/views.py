from django.views import generic

from .models import UrlPair


class IndexView(generic.CreateView):
    """Creation view for URL Cut..."""
    model = UrlPair
    template_name = 'urlcut/index.html'
    fields = ['full_url', 'usage_count_limit']

    def form_valid(self, form):
        """We need to render the same form but with generated short URL and the rest of the form filled..."""
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


class URLView(generic.DetailView):
    model = UrlPair
    template_name = 'urlcut/detail.html'

