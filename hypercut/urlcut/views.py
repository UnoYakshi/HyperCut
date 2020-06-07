"""
Handles URL pairs functionality:
- creation: creates a URL pair with URL to shorten and usage limit to provided
- removing: removes a URL pair
- detailing: displays complete a URL pair's info
- redirecting: uses short URLs (hashes) to redirect to full URLs
- listing: paginated and sorted
"""

from django.views import generic
from django.shortcuts import get_object_or_404

from .models import UrlPair
from .hash import decode


class IndexView(generic.CreateView):
    """Handles URL pairs creation..."""
    model = UrlPair
    template_name = 'urlcut/index.html'
    fields = ['full_url', 'usage_count_limit']

    def form_valid(self, form):
        """We need to render the same form but with short URL generated and the rest of the form filled..."""
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


class URLView(generic.DetailView):
    """Handles detailed description for URL pairs..."""
    model = UrlPair
    template_name = 'urlcut/detail.html'


class RemoveURLView(generic.DeleteView):
    """Handles removing URL pairs..."""
    model = UrlPair
    template_name = 'urlcut/delete.html'
    success_url = '/all-list'


class ShortURLRedirectView(generic.RedirectView):
    """ss"""
    def get_redirect_url(*args, **kwargs):
        # Determine the ID of short URL...
        short_url = kwargs.get('short_url')
        pair_id = decode(short_url)
        # Get the corresponding URL pair...
        # Note: We could find the exact pair by filtering with short URL
        #       but we suppose we don't have this field in the database...
        url_pair = get_object_or_404(UrlPair, pk=pair_id)

        # Check if usage count limit is not exceeded...
        if (url_pair.usage_count_limit > 0
                and not url_pair.usage_count < url_pair.usage_count_limit):
            return None

        url_pair.update_usage_count()
        return url_pair.full_url


class AllURLsView(generic.ListView):
    """Display all the available URL pairs. Has pagination and sorted by usage count (frequent ones go first)..."""
    model = UrlPair
    template_name = 'urlcut/all_links.html'
    context_object_name = 'url_pair_list'
    queryset = UrlPair.objects.all()
    ordering = ['-usage_count']
    paginate_by = 6
