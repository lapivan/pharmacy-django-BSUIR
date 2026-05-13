import logging
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from content.infrastructure import Infrastructure
from .models import News, CompanyInfo, FAQ, Promocode, Review, Vacancy
from .forms import NewsForm, CompanyInfoForm, FAQForm, PromocodeForm, ReviewForm, VacancyForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

logger = logging.getLogger('main')

class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'employee')
    
class StaffOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
            
        return (
            user.is_superuser or 
            user.role in ['employee', 'admin'] or 
            hasattr(user, 'employee')
        )

# News block.
class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'

    def get_queryset(self):
        logger.debug("Запрошен список новостей")
        return super().get_queryset()

class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'

class NewsCreateView(AdminOnlyMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news_form.html'
    # вычисляет url при первом использовании (лениво).
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} создал новость: {self.object.header}")
        return response

class NewsUpdateView(AdminOnlyMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} обновил новость: {self.object.header}")
        return response

class NewsDeleteView(AdminOnlyMixin, DeleteView):
    model = News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.info(f"Администратор {request.user} удалил новость: {obj.header}")
        return super().delete(request, *args, **kwargs)

# Company info block.
class CompanyInfoView(DetailView):
    model = CompanyInfo
    template_name = 'company_info.html'
    context_object_name = 'company'

    def get_object(self, queryset=None):
        return CompanyInfo.objects.first()

class CompanyInfoUpdateView(AdminOnlyMixin, UpdateView):
    model = CompanyInfo
    form_class = CompanyInfoForm 
    template_name = 'company_info_form.html'
    success_url = reverse_lazy('company_info')

    def get_object(self, queryset=None):
        return CompanyInfo.objects.first() 

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} обновил информацию о компании")
        return response

# FAQ block.
class FAQView(ListView):
    model = FAQ
    template_name = 'FAQ.html'
    context_object_name = 'faq'

    def get_queryset(self):
        logger.debug("Запрошен список FAQ")
        return super().get_queryset()

class FAQCreateView(AdminOnlyMixin, CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'FAQ_form.html'
    success_url = reverse_lazy('FAQ')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} добавил новый вопрос в FAQ")
        return response

class FAQUpdateView(AdminOnlyMixin, UpdateView):
    model = FAQ
    form_class = FAQForm 
    template_name = 'FAQ_form.html'
    success_url = reverse_lazy('FAQ')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} обновил вопрос в FAQ (ID: {self.object.id})")
        return response

class FAQDeleteView(AdminOnlyMixin, DeleteView):
    model = FAQ
    template_name = 'FAQ_confirm_delete.html'
    success_url = reverse_lazy('FAQ')

    def delete(self, request, *args, **kwargs):
        logger.info(f"Администратор {request.user} удалил запись из FAQ (ID: {self.get_object().id})")
        return super().delete(request, *args, **kwargs)

# Vacancy block
class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy_list.html'
    context_object_name = 'vacancies'
    def get_queryset(self):
        logger.debug("Запрошен список вакансий")
        return Vacancy.objects.filter(is_active=True).order_by('-created_at')

class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancy_detail.html'

class VacancyCreateView(AdminOnlyMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancy_form.html'
    success_url = reverse_lazy('vacancy_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} создал вакансию: {self.object.title}")
        return response

class VacancyUpdateView(AdminOnlyMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancy_form.html'
    success_url = reverse_lazy('vacancy_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} обновил вакансию: {self.object.title}")
        return response

class VacancyDeleteView(AdminOnlyMixin, DeleteView):
    model = Vacancy
    template_name = 'vacancy_confirm_delete.html'
    success_url = reverse_lazy('vacancy_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.info(f"Администратор {request.user} удалил вакансию: {obj.title}")
        return super().delete(request, *args, **kwargs)

# Review block
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    ordering = ['-date']

    def get_queryset(self):
        logger.debug("Запрошен список отзывов")
        return super().get_queryset()

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Пользователь {self.request.user} оставил отзыв")
        return response

class ReviewDeleteView(AdminOnlyMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

    def delete(self, request, *args, **kwargs):
        logger.info(f"Администратор {request.user} удалил отзыв (ID: {self.get_object().id})")
        return super().delete(request, *args, **kwargs)

# Promocode block
class PromocodeListView(ListView):
    model = Promocode
    template_name = 'promocode_list.html'
    context_object_name = 'promocodes'

class PromocodeCreateView(AdminOnlyMixin, CreateView):
    model = Promocode
    form_class = PromocodeForm
    template_name = 'promocode_form.html'
    success_url = reverse_lazy('promocode_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} создал промокод: {self.object.code}")
        return response

class PromocodeUpdateView(AdminOnlyMixin, UpdateView):
    model = Promocode
    form_class = PromocodeForm
    template_name = 'promocode_form.html'
    success_url = reverse_lazy('promocode_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Администратор {self.request.user} обновил промокод: {self.object.code}")
        return response

class PromocodeDeleteView(AdminOnlyMixin, DeleteView):
    model = Promocode
    template_name = 'promocode_confirm_delete.html'
    success_url = reverse_lazy('promocode_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.info(f"Администратор {request.user} удалил промокод: {obj.code}")
        return super().delete(request, *args, **kwargs)

class PrivacyPolicyView(TemplateView):
    template_name = "privacy.html"
    
    def get(self, request, *args, **kwargs):
        logger.debug("Просмотр политики конфиденциальности")
        return super().get(request, *args, **kwargs)
    
class PerformanceView(TemplateView):
    template_name = 'performance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_a_results = Infrastructure.run_threading_test()
        task_b_results = Infrastructure.run_multiprocessing_test()
        task_c_results = Infrastructure.run_asyncio_test()
        
        context['task_a'] = task_a_results
        context['task_b'] = task_b_results
        context['task_c'] = task_c_results
        
        return context