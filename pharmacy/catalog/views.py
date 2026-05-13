import calendar
import logging
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import transaction
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from catalog.services import ExternalAPIService, StatisticsService
from content.views import AdminOnlyMixin, StaffOnlyMixin, StaffOrAdminRequiredMixin
from .forms import CategoryForm, DepartmentForm, EmployeeForm, MedicineForm, SaleForm, SaleItemFormSet, SupplierForm
from .models import Category, Department, Employee, Medicine, Sale, Supplier

logger = logging.getLogger('main')

# Medicines
class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine_list.html'
    context_object_name = 'medicines'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')
        supplier_id = self.request.GET.get('supplier', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')

        if search_query:
            logger.debug(f"Выполнен поиск медикаментов по запросу: '{search_query}'")
            queryset = queryset.filter(name__icontains=search_query)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        now_utc = timezone.now()
        now_local = timezone.localtime(now_utc)
        
        context['current_time_utc'] = now_utc
        context['current_time_local'] = now_local
        context['user_timezone'] = timezone.get_current_timezone_name()
        
        cal = calendar.TextCalendar(calendar.MONDAY)
        context['text_calendar'] = cal.formatmonth(now_utc.year, now_utc.month)
        
        context['categories'] = Category.objects.all()
        context['suppliers'] = Supplier.objects.all()
        context['departments'] = Department.objects.all()
        
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(AdminOnlyMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(AdminOnlyMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(AdminOnlyMixin, DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

class MedicineDetailView(DetailView):
    model = Medicine
    template_name = 'medicine_detail.html'

class MedicineCreateView(AdminOnlyMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine_form.html'
    success_url = reverse_lazy('medicine_list')

class MedicineUpdateView(AdminOnlyMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine_form.html'
    success_url = reverse_lazy('medicine_list')

class MedicineDeleteView(AdminOnlyMixin, DeleteView):
    model = Medicine
    template_name = 'medicine_confirm_delete.html'
    success_url = reverse_lazy('medicine_list')

# Departments
class DepartmentListView(ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(AdminOnlyMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentUpdateView(AdminOnlyMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'department_form.html'
    success_url = reverse_lazy('department_list')

class DepartmentDeleteView(AdminOnlyMixin, DeleteView):
    model = Department
    template_name = 'department_confirm_delete.html'
    success_url = reverse_lazy('department_list')

# Employees
class EmployeeListView(AdminOnlyMixin, ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'employee_detail.html'
    context_object_name = 'employee'

class EmployeeCreateView(AdminOnlyMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].required = True
        return form
    
class ContactListView(ListView):
    model = Employee
    template_name = 'contacts.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.select_related('user__profile', 'department').all()

class EmployeeUpdateView(AdminOnlyMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(AdminOnlyMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

# Suppliers
class SupplierListView(StaffOrAdminRequiredMixin, ListView):
    model = Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(StaffOrAdminRequiredMixin, DetailView):
    model = Supplier
    template_name = 'supplier_detail.html'

class SupplierCreateView(AdminOnlyMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierUpdateView(AdminOnlyMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier_form.html'
    success_url = reverse_lazy('supplier_list')

class SupplierDeleteView(AdminOnlyMixin, DeleteView):
    model = Supplier
    template_name = 'supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')

# Sales
class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SaleItemFormSet(self.request.POST)
        else:
            data['items'] = SaleItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        
        if form.is_valid() and items.is_valid():
            valid_items = [f for f in items.forms if f.cleaned_data and not f.cleaned_data.get('DELETE')]
            if not valid_items:
                logger.warning(f"Пользователь {self.request.user} попытался создать пустой заказ.")
                messages.error(self.request, "Заказ не может быть пустым!")
                return self.render_to_response(self.get_context_data(form=form))

            promo_code = form.cleaned_data.get('applied_promocode')
            if promo_code:
                from content.models import Promocode
                promo = Promocode.objects.filter(code=promo_code, is_active=True).first()
                if not promo:
                    logger.warning(f"Неудачная попытка применить промокод '{promo_code}' пользователем {self.request.user}")
                    messages.error(self.request, f"Промокод '{promo_code}' не существует или неактивен!")
                    return self.render_to_response(self.get_context_data(form=form))

            try:
                with transaction.atomic():
                    for item_form in valid_items:
                        medicine = item_form.cleaned_data['medicine']
                        quantity = item_form.cleaned_data['quantity']
                        if medicine.stock_quantity < quantity:
                            raise ValueError(f"На складе недостаточно товара: {medicine.name}")

                    form.instance.client = self.request.user
                    if hasattr(self.request.user, 'employee'):
                        form.instance.employee = self.request.user.employee
                    
                    self.object = form.save()
                    items.instance = self.object
                    
                    item_instances = items.save(commit=False)
                    for instance in item_instances:
                        instance.price_at_sale = instance.medicine.price
                        instance.medicine.stock_quantity -= instance.quantity
                        instance.medicine.save()
                        instance.save()
                    
                    items.save_m2m()

                logger.info(f"Пользователь {self.request.user} успешно оформил заказ #{self.object.id}")
                messages.success(self.request, "Покупка успешно оформлена!")
                return redirect('medicine_list')

            except ValueError as e:
                logger.error(f"Ошибка при оформлении заказа пользователем {self.request.user}: {e}")
                messages.error(self.request, str(e))
                return self.render_to_response(self.get_context_data(form=form))
        else:
            logger.warning(f"Ошибка валидации формы заказа у пользователя {self.request.user}")
            return self.render_to_response(self.get_context_data(form=form, items=items))
        
class EmployeeSalesListView(StaffOnlyMixin, ListView):
    model = Sale
    template_name = 'employee_sales_list.html'
    context_object_name = 'sales'
    paginate_by = 15

    def get_queryset(self):
        return Sale.objects.filter(employee__user=self.request.user).select_related('client', 'department').order_by('-sale_date')
        
class UserPurchaseHistoryView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'user_sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10

    def get_queryset(self):
        return Sale.objects.filter(client=self.request.user).select_related('employee', 'department').order_by('-created_at')
    
class AnalyticsDashboardView(AdminOnlyMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        logger.info(f"Администратор {self.request.user} открыл дашборд аналитики.")
        context = super().get_context_data(**kwargs)
        
        context['revenue'] = StatisticsService.get_total_revenue()  
        context['sales_stats'] = StatisticsService.get_sale_aggregations()
        context['age_stats'] = StatisticsService.get_client_age_stats()
        context['insights'] = StatisticsService.get_product_insights()
        context['chart'] = StatisticsService.get_sales_chart()
        
        context['medicines_alphabetical'] = Medicine.objects.annotate(
            total_sales_sum=Sum(
                ExpressionWrapper(
                    F('saleitem__price_at_sale') * F('saleitem__quantity'),
                    output_field=FloatField()
                )
            )
        ).order_by('name')
        
        return context
    
class GlobalMedicalNewsView(TemplateView):
    template_name = 'global_news.html'

    def get_context_data(self, **kwargs):
        logger.info("Загрузка страницы мировых новостей медицины.")
        context = super().get_context_data(**kwargs)
        context['external_articles'] = ExternalAPIService.get_medical_news()
        context['dog_image'] = ExternalAPIService.get_random_dog()
        return context
    
class AdditionalServicesView(TemplateView):
    template_name = 'services.html'