from django.db import models


class Testimonial(models.Model):
    RATING_CHOICES = [
        (5, '5 Stars'),
        (4, '4 Stars'),
        (3, '3 Stars'),
        (2, '2 Stars'),
        (1, '1 Star'),
    ]

    customer_name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.customer_name} - {self.service}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question
