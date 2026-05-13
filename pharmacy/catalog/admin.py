from django.contrib import admin
from .models import Category, Supplier, Department, Medicine, Employee, EmployeeProfile, Sale, SaleItem

class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация (Профиль)'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'created_at')
    list_filter = ('department', 'position')
    search_fields = ('full_name', 'user__username')
    inlines = [EmployeeProfileInline]

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('price_at_sale',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'total_amount', 'sale_date')
    list_filter = ('sale_date', 'employee', 'department')
    search_fields = ('client__username', 'applied_promocode')
    inlines = [SaleItemInline]
    readonly_fields = ('sale_date',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'supplier')
    list_filter = ('category', 'supplier', 'department')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone_number', 'email')
    search_fields = ('name', 'contact_person')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')