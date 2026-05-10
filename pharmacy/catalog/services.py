from datetime import date, timedelta
import os
import statistics
import logging
import requests
from .models import Sale, SaleItem, Medicine, Department
from django.db.models import Sum, Avg, Count, F, FloatField, ExpressionWrapper
from django.contrib.auth import get_user_model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

logger = logging.getLogger('main')

class StatisticsService:
    @staticmethod
    def get_sale_aggregations():
        sales_data = SaleItem.objects.values('sale_id').annotate(
            total=Sum(ExpressionWrapper(F('quantity') * F('price_at_sale'), output_field=FloatField()))
        ).values_list('total', flat=True)

        amounts = list(sales_data)
        if not amounts:
            return {'mean': 0, 'median': 0}
        
        return {
            'mean': sum(amounts) / len(amounts),
            'median': statistics.median(amounts),
        }
    
    @staticmethod
    def get_total_revenue():
        total_revenue = SaleItem.objects.aggregate(
            total=Sum(ExpressionWrapper(F('quantity') * F('price_at_sale'), output_field=FloatField()))
        )['total'] or 0
        
        revenue_by_dept = Department.objects.annotate(
            dept_revenue=Sum(ExpressionWrapper(F('sales__items__quantity') * F('sales__items__price_at_sale'), output_field=FloatField()))
        ).values('name', 'dept_revenue')
        
        logger.info("Выполнен расчет общей выручки")
        return {
            'total_revenue': total_revenue,
            'revenue_by_dept': list(revenue_by_dept)
        }

    @staticmethod
    def get_product_insights():
        most_popular = SaleItem.objects.values('medicine__category__name') \
            .annotate(total_qty=Sum('quantity')) \
            .order_by('-total_qty').first()
            
        most_profitable = SaleItem.objects.values('medicine__category__name') \
            .annotate(total_profit=Sum(ExpressionWrapper(F('quantity') * F('price_at_sale'), output_field=FloatField()))) \
            .order_by('-total_profit').first()
            
        return {
            'most_popular': most_popular,
            'most_profitable': most_profitable
        }
    
    @staticmethod
    def get_client_age_stats():
        birth_dates = get_user_model().objects.filter(role='client', date_of_birth__isnull=False).values_list('date_of_birth', flat=True)
        today = date.today()
        ages = [today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day)) for bd in birth_dates]
        if not ages: return {'mean_age': 0, 'median_age': 0}
        return {'mean_age': statistics.mean(ages), 'median_age': statistics.median(ages)}
    
    @staticmethod
    def get_sales_chart():
        data = SaleItem.objects.values('medicine__category__name').annotate(
            total=Sum(ExpressionWrapper(F('quantity') * F('price_at_sale'), output_field=FloatField()))
        ).order_by('-total')

        if not data:
            return None

        categories = [item['medicine__category__name'] or "Без категории" for item in data]
        totals = [item['total'] for item in data]

        plt.figure(figsize=(6, 6))
        plt.pie(totals, labels=categories, autopct="%1.1f%%", colors=["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b"])
        plt.title("Доля выручки по категориям")

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.clf()
        plt.close()

        logger.info("Сгенерирован график продаж")
        return base64.b64encode(image_png).decode('utf-8')

class ExternalAPIService:
    @staticmethod
    def get_medical_news():
        api_key = os.getenv("EXTERNAL_API_KEY")
        week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        url = f"https://newsapi.org/v2/everything?q=medicine&from={week_ago}&language=ru&apiKey={api_key}"
        try:
            logger.debug(f"Запрос новостей по адресу: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json().get('articles', [])[:12]
            else:
                logger.warning(f"News API вернул код {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при обращении к News API: {e}")
        return []
    
    @staticmethod
    def get_random_dog():
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random", timeout=3)
            if response.status_code == 200:
                return response.json().get('message')
            logger.warning(f"Dogs API вернул код {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при обращении к Dogs API: {e}")
        return None