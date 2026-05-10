from django.urls import re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Medicines
    re_path(r'^medicines/$', views.MedicineListView.as_view(), name='medicine_list'),
    re_path(r'^medicines/(?P<pk>\d+)/$', views.MedicineDetailView.as_view(), name='medicine_detail'),
    re_path(r'^medicines/add/$', views.MedicineCreateView.as_view(), name='medicine_create'),
    re_path(r'^medicines/(?P<pk>\d+)/edit/$', views.MedicineUpdateView.as_view(), name='medicine_update'),
    re_path(r'^medicines/(?P<pk>\d+)/delete/$', views.MedicineDeleteView.as_view(), name='medicine_delete'),

    # Employees
    re_path(r'^employees/$', views.EmployeeListView.as_view(), name='employee_list'),
    re_path(r'^employees/(?P<pk>\d+)/$', views.EmployeeDetailView.as_view(), name='employee_detail'),
    re_path(r'^employees/add/$', views.EmployeeCreateView.as_view(), name='employee_create'),
    re_path(r'^employees/(?P<pk>\d+)/edit/$', views.EmployeeUpdateView.as_view(), name='employee_update'),
    re_path(r'^employees/(?P<pk>\d+)/delete/$', views.EmployeeDeleteView.as_view(), name='employee_delete'),

    # Departments
    re_path(r'^departments/$', views.DepartmentListView.as_view(), name='department_list'),
    re_path(r'^departments/add/$', views.DepartmentCreateView.as_view(), name='department_create'),
    re_path(r'^departments/(?P<pk>\d+)/edit/$', views.DepartmentUpdateView.as_view(), name='department_update'),
    re_path(r'^departments/(?P<pk>\d+)/delete/$', views.DepartmentDeleteView.as_view(), name='department_delete'),

    # Suppliers
    re_path(r'^suppliers/$', views.SupplierListView.as_view(), name='supplier_list'),
    re_path(r'^suppliers/(?P<pk>\d+)/$', views.SupplierDetailView.as_view(), name='supplier_detail'),
    re_path(r'^suppliers/add/$', views.SupplierCreateView.as_view(), name='supplier_create'),
    re_path(r'^suppliers/(?P<pk>\d+)/edit/$', views.SupplierUpdateView.as_view(), name='supplier_update'),
    re_path(r'^suppliers/(?P<pk>\d+)/delete/$', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Sales
    re_path(r'^sales/add/$', views.SaleCreateView.as_view(), name='sale_create'),
    re_path(r'^my-purchases/$', views.UserPurchaseHistoryView.as_view(), name='user_purchases'),
    re_path(r'^my-sales/$', views.EmployeeSalesListView.as_view(), name='employee_sales'),
    
    # Analytics
    re_path(r'^dashboard/$', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    
    # Contacts
    re_path(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),

    # Categories
    re_path(r'^categories/$', views.CategoryListView.as_view(), name='category_list'),
    re_path(r'^categories/add/$', views.CategoryCreateView.as_view(), name='category_create'),
    re_path(r'^categories/(?P<pk>\d+)/edit/$', views.CategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^categories/(?P<pk>\d+)/delete/$', views.CategoryDeleteView.as_view(), name='category_delete'),

    # News
    re_path(r'^global-news/$', views.GlobalMedicalNewsView.as_view(), name='global_news'),

    re_path(r'^additional-services/$', views.AdditionalServicesView.as_view(), name='additional_services'),
]