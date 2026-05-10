from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from catalog.models import TimeStampedModel

class CompanyInfo(TimeStampedModel):
    name_full = models.CharField(max_length=100, verbose_name="Full Name")
    name_short = models.CharField(max_length=50, verbose_name="Short Name")
    main_info = models.TextField(verbose_name="Main Description")
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    history = models.TextField(verbose_name="Company History")
    details = models.CharField(max_length=255, verbose_name="Legal Details")

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.name_short

class News(TimeStampedModel):
    header = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    news_text = models.TextField()
    logo = models.ImageField(upload_to='news/', blank=True, null=True)
    publication_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "News Article"
        verbose_name_plural = "News"
        ordering = ['-publication_date']

    def __str__(self):
        return self.header

class FAQ(TimeStampedModel):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question[:50]

class Vacancy(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title

class Promocode(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Promocode"
        verbose_name_plural = "Promocodes"

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"

    def calculate_discount(self, amount):
        from decimal import Decimal
        return amount * (Decimal(1) - (Decimal(self.discount_percent) / Decimal(100)))

class Review(TimeStampedModel):
    username = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.username} - {self.rating} stars"