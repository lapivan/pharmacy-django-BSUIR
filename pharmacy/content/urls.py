from django.urls import re_path
from .views import *

urlpatterns = [
    # News
    re_path(r'^news/$', NewsListView.as_view(), name='news_list'),
    re_path(r'^news/(?P<pk>\d+)/$', NewsDetailView.as_view(), name='news_detail'),
    re_path(r'^news/add/$', NewsCreateView.as_view(), name='news_create'),
    re_path(r'^news/(?P<pk>\d+)/edit/$', NewsUpdateView.as_view(), name='news_update'),
    re_path(r'^news/(?P<pk>\d+)/delete/$', NewsDeleteView.as_view(), name='news_delete'),

    # Company info
    re_path(r'^info/$', CompanyInfoView.as_view(), name='company_info'),
    re_path(r'^info/edit/$', CompanyInfoUpdateView.as_view(), name='company_info_update'),

    # FAQ
    re_path(r'^faq/$', FAQView.as_view(), name='FAQ'),
    re_path(r'^faq/add/$', FAQCreateView.as_view(), name='FAQ_create'),
    re_path(r'^faq/(?P<pk>\d+)/edit/$', FAQUpdateView.as_view(), name='FAQ_update'),
    re_path(r'^faq/(?P<pk>\d+)/delete/$', FAQDeleteView.as_view(), name='FAQ_delete'),

    # Vacancies
    re_path(r'^vacancies/$', VacancyListView.as_view(), name='vacancy_list'),
    re_path(r'^vacancies/(?P<pk>\d+)/$', VacancyDetailView.as_view(), name='vacancy_detail'),
    re_path(r'^vacancies/add/$', VacancyCreateView.as_view(), name='vacancy_create'),
    re_path(r'^vacancies/(?P<pk>\d+)/edit/$', VacancyUpdateView.as_view(), name='vacancy_update'),
    re_path(r'^vacancies/(?P<pk>\d+)/delete/$', VacancyDeleteView.as_view(), name='vacancy_delete'),

    # Reviews
    re_path(r'^reviews/$', ReviewListView.as_view(), name='review_list'),
    re_path(r'^reviews/add/$', ReviewCreateView.as_view(), name='review_create'),
    re_path(r'^reviews/(?P<pk>\d+)/delete/$', ReviewDeleteView.as_view(), name='review_delete'),

    # Promocodes
    re_path(r'^promocodes/$', PromocodeListView.as_view(), name='promocode_list'),
    re_path(r'^promocodes/add/$', PromocodeCreateView.as_view(), name='promocode_create'),
    re_path(r'^promocodes/(?P<pk>\d+)/edit/$', PromocodeUpdateView.as_view(), name='promocode_update'),
    re_path(r'^promocodes/(?P<pk>\d+)/delete/$', PromocodeDeleteView.as_view(), name='promocode_delete'),

    # Privacy
    re_path(r'^privacy/$', PrivacyPolicyView.as_view(), name='privacy'),

    # Perfomance
    re_path(r'^performance/$', PerformanceView.as_view(), name='performance_test'),
]