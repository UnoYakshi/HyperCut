from django.db import models
from django.urls import reverse

from .hash import encode


class UrlPair(models.Model):
    """Full-short URLs pair. Main entity for the entire application..."""
    full_url = models.URLField(null=False)
    short_url = models.CharField(max_length=50, unique=True, db_index=True)

    usage_count = models.IntegerField(default=0, null=True)
    usage_count_limit = models.IntegerField(default=-1, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def update_usage_count(self):
        self.usage_count += 1
        self.save()

    def save(self, *args, **kwargs):
        """Re-overwrite: fill in short URL using the provided full URL..."""
        super(UrlPair, self).save(*args, **kwargs)
        hashed = encode(self.id)
        self.short_url = hashed
        super(UrlPair, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Re-overwrite: can call specific instance's details from any project's part with an absolute path..."""
        return reverse('detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.short_url} :: {self.full_url}'
