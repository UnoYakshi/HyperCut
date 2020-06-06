from django.views import generic
from django.shortcuts import get_object_or_404

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


class ShortURLRedirectView(generic.RedirectView):
    pattern_name = 'url-redirect'

    def get_redirect_url(*args, **kwargs):
        short_url = kwargs.get('short_url')
        url_pair = get_object_or_404(UrlPair, short_url=short_url)
        url_pair.update_usage_count()
        return url_pair.full_url


class URLView(generic.DetailView):
    model = UrlPair
    template_name = 'urlcut/detail.html'
