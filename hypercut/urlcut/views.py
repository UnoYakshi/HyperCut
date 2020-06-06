from django.views import generic

from .models import UrlPair


class IndexView(generic.CreateView):
    model = UrlPair
    template_name = 'urlcut/index.html'
    fields = ['full_url', 'usage_count_limit']
