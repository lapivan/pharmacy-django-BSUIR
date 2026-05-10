import pytest
from decimal import Decimal
from django.urls import reverse
from users.models import User
from content.models import Promocode, Review, FAQ, News


@pytest.mark.django_db
class TestContentModels:

    def test_promocode_discount(self):
        promo = Promocode.objects.create(
            code='SALE10',
            discount_percent=10
        )

        result = promo.calculate_discount(Decimal('100'))

        assert result == Decimal('90')

    def test_review_str(self):
        review = Review.objects.create(
            username='ivan',
            text='good',
            rating=5
        )

        assert str(review) == 'Review by ivan - 5 stars'

    def test_faq_str(self):
        faq = FAQ.objects.create(
            question='What is this question?',
            answer='Answer'
        )

        assert 'What is this question?' in str(faq)


@pytest.mark.django_db
class TestContentViews:

    def test_news_list_view(self, client):
        News.objects.create(
            header='Test news',
            short_description='Short',
            news_text='Full text'
        )

        response = client.get(reverse('news_list'))

        assert response.status_code == 200
        assert 'news_list' in response.context

    def test_news_detail_view(self, client):
        news = News.objects.create(
            header='Test news',
            short_description='Short',
            news_text='Full text'
        )

        response = client.get(reverse('news_detail', args=[news.id]))

        assert response.status_code == 200

    def test_admin_only_create_news(self, client):
        response = client.get(reverse('news_create'))

        assert response.status_code in [302, 403]

    def test_admin_can_create_news(self, client):
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )

        client.login(username='admin', password='admin123')

        response = client.post(reverse('news_create'), {
            'header': 'Admin News',
            'short_description': 'Short',
            'news_text': 'Text',
            'publication_date': '2025-01-01'
        })

        assert response.status_code == 302
        assert News.objects.filter(header='Admin News').exists()