from django import forms
from .models import Category, Medicine, Department, Supplier, Sale

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'supplier', 'department', 'description','instruction', 'price', 'photo', 'stock_quantity']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'location']

from django.contrib.auth import get_user_model
from .models import Employee, EmployeeProfile

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Логин (Username)")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Пароль",
        help_text="Оставьте пустым при редактировании, если не хотите менять пароль."
    )

    salary = forms.DecimalField(max_digits=10, decimal_places=2, label="Зарплата")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Дата рождения"
    )

    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            
            if hasattr(self.instance, 'profile'):
                self.fields['salary'].initial = self.instance.profile.salary
                self.fields['date_of_birth'].initial = self.instance.profile.date_of_birth

    def save(self, commit=True):
            User = get_user_model()
            
            if not self.instance.pk:
                user = User.objects.create_user(
                    username=self.cleaned_data['username'],
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password'],
                    role='employee',
                    date_of_birth=self.cleaned_data['date_of_birth']
                )
                employee = super().save(commit=False)
                employee.user = user
            else:
                employee = super().save(commit=False)
                user = employee.user
                user.username = self.cleaned_data['username']
                user.email = self.cleaned_data['email']
                user.date_of_birth = self.cleaned_data['date_of_birth'] 
                
                if self.cleaned_data.get('password'):
                    user.set_password(self.cleaned_data['password'])
                user.save()

            if commit:
                employee.save()
                profile, created = EmployeeProfile.objects.update_or_create(
                    employee=employee, 
                    defaults={
                        'salary': self.cleaned_data['salary'],
                        'date_of_birth': self.cleaned_data['date_of_birth']
                    }
                )

            return employee
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone_number', 'email']

from django import forms
from django.forms import inlineformset_factory
from .models import Sale, SaleItem, Employee

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['department', 'employee', 'applied_promocode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].required = False
        self.fields['department'].required = True

SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem,
    fields=['medicine', 'quantity'],
    extra=3,
    can_delete=True
)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание',
        }