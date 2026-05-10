from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('employee', 'Employee'),
        ('admin', 'Administrator'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    date_of_birth = models.DateField(null=True, blank=True)
    
    phone_regex = RegexValidator(
        regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
        message="Phone number must be in format: '+375 (XX) XXX-XX-XX'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def clean(self):
        super().clean()
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age < 18:
                raise ValidationError("Users must be at least 18 years old.")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"