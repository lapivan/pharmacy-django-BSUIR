from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date
from django.conf import settings

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Supplier(TimeStampedModel):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+375 \((29|33|44|25)\) \d{3}-\d{2}-\d{2}$',
        message="Phone number must be in format: '+375 (XX) XXX-XX-XX'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Department(TimeStampedModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Medicine(TimeStampedModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='medicines')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='medicines')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='medicines')
    description = models.TextField()
    instruction = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='medicines/', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Employee(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')
    full_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    department = models.ForeignKey(
        'Department', 
        on_delete=models.SET_NULL,
        null=True, 
        related_name='employees',
        verbose_name="Department"
    )

    def __str__(self):
        return self.full_name
    
class EmployeeProfile(TimeStampedModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField()
    def clean(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            if age < 18:
                raise ValidationError("Employee must be at least 18 years old.")

class Sale(TimeStampedModel):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='sales')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sales', null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    sale_date = models.DateTimeField(auto_now_add=True)
    
    applied_promocode = models.CharField(max_length=50, blank=True, null=True, verbose_name="Promocode")

    @property
    def total_amount(self):
        total = sum(item.get_cost() for item in self.items.all())
        
        if self.applied_promocode:
            from content.models import Promocode
            
            promo = Promocode.objects.filter(code=self.applied_promocode, is_active=True).first()
            if promo:
                total = promo.calculate_discount(total)
        
        return round(total, 2)

    def __str__(self):
        return f"Sale #{self.id} - {self.client.username}"

class SaleItem(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        return self.price_at_sale * self.quantity

    def save(self, *args, **kwargs):
        if not self.price_at_sale:
            self.price_at_sale = self.medicine.price
        super().save(*args, **kwargs)