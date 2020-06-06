from django.db import models
import short_url


class UrlPair(models.Model):
    """Full-short URLs pair. Main entity for the entire application..."""
    full_url = models.TextField()
    short_url = models.CharField(max_length=50, unique=True, db_index=True)

    usage_count = models.IntegerField(default=0, null=True)
    usage_count_limit = models.IntegerField(default=-1, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Shorten the given full URL...
        self.short_url = short_url.encode_url(self.full_url)
        super(UrlPair, self).save(*args, **kwargs)
