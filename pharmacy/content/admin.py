from django.contrib import admin
from .models import CompanyInfo, News, FAQ, Vacancy, Promocode, Review

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name_short', 'name_full', 'details')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('header', 'publication_date')
    search_fields = ('header', 'news_text')
    list_filter = ('publication_date',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'rating', 'date')
    list_filter = ('rating', 'date')