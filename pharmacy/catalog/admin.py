from django.contrib import admin
from .models import (
    Category, Supplier, Department, Medicine, 
    Employee, EmployeeProfile, Sale, SaleItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone_number', 'email')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'department')
    search_fields = ('name', 'description', 'instruction')
    list_filter = ('category', 'department', 'supplier')
    list_editable = ('price', 'stock_quantity')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department')
    search_fields = ('full_name', 'user__username')
    list_filter = ('department',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'hire_date', 'date_of_birth')
    search_fields = ('employee__full_name',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('price_at_sale',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'department', 'sale_date')
    list_filter = ('sale_date', 'department')
    search_fields = ('client__username', 'employee__full_name')
    readonly_fields = ('sale_date',)
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'medicine', 'quantity', 'price_at_sale')
    search_fields = ('sale__id', 'medicine__name')