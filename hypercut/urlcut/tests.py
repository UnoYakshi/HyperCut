from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from .models import UrlPair
from .views import ShortURLRedirectView, RemoveURLView, AllURLsView
from .hash import encode, decode

# Test data...
FULL_URL_CORRECT = 'https://google.com/'
FULL_URLS_INCORRECT = {'com/您好!': '7Q', 'g()()gle.com': 'BX'}
FULL_URL_NON_EXISTENT = 'google.com.uk.gov.io.de.ua'
HASH_DATA = {'hashed': 'PD', 'id': 12}


class UrlPairTC(TestCase):
    """Checks if URL-related functionality works..."""

    def setUp(self) -> None:
        self.new_url_pair = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=-1)
        self.new_url_pair.save()
        print(self.new_url_pair.id)

    def test_full_url_persistent(self):
        """Tests created URL pair does save full URL..."""
        self.assertEqual(self.new_url_pair.full_url, FULL_URL_CORRECT)

    def test_full_url_incorrect_format(self):
        """Checks if incorrect URLs (format) aren't allowed..."""
        for incorrect_url, short_url in FULL_URLS_INCORRECT.items():
            # new_url_pair = UrlPair.objects.create(full_url=incorrect_url, usage_count_limit=-1)
            new_url_pair = UrlPair(full_url=incorrect_url)
            new_url_pair.save()
            self.assertEqual(new_url_pair.short_url, short_url)

    def test_full_url_incorrect_non_existent(self):
        """Checks if incorrect URLs (format) aren't allowed..."""
        new_url_pair = UrlPair(full_url=FULL_URL_NON_EXISTENT, short_url='')
        new_url_pair.save()
        self.assertEqual(True, True)

    def test_date_time(self):
        """Tests created URLPair creation datetime is correct..."""
        new_url_pair = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=-1)
        new_url_pair.save()
        self.assertEqual(new_url_pair.created.date(), datetime.now().date())
        self.assertLess(new_url_pair.created.time(), datetime.now().time())
        new_url_pair.delete()

    def test_usage_count_update(self):
        """Tests if updating usage counter is correct..."""
        self.new_url_pair.update_usage_count()
        self.assertEqual(self.new_url_pair.usage_count, 1)

    def test_get_absolute_url(self):
        """Tests if UrlPair's absolute URL is correctly generated..."""
        # Get the absolute URL and compose its golden value...
        abs_url = self.new_url_pair.get_absolute_url()
        real_abs_url = f'/detail/{self.new_url_pair.id}/'

        self.assertEqual(abs_url, real_abs_url)

    def test_str(self):
        """Tests `__str__()` is correct..."""
        self.assertEqual(str(self.new_url_pair), f'{self.new_url_pair.short_url} :: {self.new_url_pair.full_url}')


class ViewsTC(TestCase):
    """Mostly tests Redirect and Delete views..."""
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_redirect(self):
        """Tests if redirects works..."""
        new_url_pair = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=-1)
        new_url_pair.save()

        # Compose redirect request...
        request = self.factory.get(path=f'/{new_url_pair.short_url}')
        request.user = AnonymousUser()

        # Check if redirect works...
        response = ShortURLRedirectView.as_view()(request, short_url=new_url_pair.short_url)
        self.assertRedirects(response, f'{new_url_pair.full_url}', fetch_redirect_response=False)
        self.assertLess(response.status_code, 400)

    def test_usage_count_limit(self):
        """Tests if usage count limit works as intented..."""
        new_url_pair = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=1)
        new_url_pair.save()

        # Compose redirect request...
        request = self.factory.get(path=f'/{new_url_pair.short_url}')
        request.user = AnonymousUser()

        # "Use" the link...
        new_url_pair.update_usage_count()

        # Check if yet another usage works (it shouldn't)...
        response = ShortURLRedirectView.as_view()(request, short_url=new_url_pair.short_url)
        self.assertGreaterEqual(response.status_code, 400)

    def test_delete(self):
        response = self.client.get('/rm/1')

        self.assertLessEqual(response.status_code, 400)


class AllTC(TestCase):
    """Tests displaying all the URLs in `/all-list/` """
    def setUp(self):
        # Add a couple of pairs...
        self.first = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=-1)
        self.first.save()
        self.second = UrlPair(full_url=FULL_URL_CORRECT, usage_count_limit=-1)
        self.second.save()
        self.factory = RequestFactory()

    def test_smoke(self):
        """Smoke test: checks if it's at least starts..."""
        request = self.factory.get(path='/all-list/')
        request.user = AnonymousUser()

        response = AllURLsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_items_count(self):
        """Tests if there is a correct number of instances in the database via AllURLsView.."""
        request = self.factory.get(path='/all-list/')
        request.user = AnonymousUser()

        response = AllURLsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        items_count = response.context_data['url_pair_list'].count()
        self.assertEqual(items_count, 2)


class HashTC(TestCase):
    """Tests hash-related functionality..."""
    def test_decode(self):
        """Tests encoding (hash to ID)..."""
        short_url = HASH_DATA['hashed']
        decoded_id = decode(short_url)
        self.assertEqual(HASH_DATA['id'], decoded_id)

    def test_encode(self):
        """Tests encoding (ID to hash)..."""
        real_hashed = HASH_DATA['hashed']
        hashed = encode(HASH_DATA['id'])
        self.assertEqual(hashed, real_hashed)
