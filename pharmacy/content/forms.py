from django import forms
from .models import News, CompanyInfo, FAQ, Promocode, Review, Vacancy

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['header', 'short_description', 'news_text', 'logo', 'publication_date']

class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = ['name_full', 'name_short', 'main_info', 'logo', 'history', 'details']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'is_active']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['username', 'text', 'rating']

class PromocodeForm(forms.ModelForm):
    class Meta:
        model = Promocode
        fields = ['code', 'discount_percent', 'is_active']