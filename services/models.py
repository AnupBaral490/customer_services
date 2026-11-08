from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    what_included = models.TextField(help_text="Comma-separated list of included items")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, help_text="e.g., 'From $99' or 'Custom quote'")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Services'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_included_items(self):
        """Return included items as a list."""
        return [item.strip() for item in self.what_included.split(',')]

    def __str__(self):
        return self.name
