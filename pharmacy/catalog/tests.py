import pytest
from decimal import Decimal
from unittest.mock import patch

from django.urls import reverse

from users.models import User
from catalog.models import (
    Category,
    Supplier,
    Department,
    Medicine,
    Sale,
    SaleItem,
)

from catalog.services import StatisticsService


@pytest.mark.django_db
class TestCatalogModels:

    def setup_method(self):
        self.category = Category.objects.create(name='Tablets')

        self.supplier = Supplier.objects.create(
            name='Supplier',
            contact_person='Ivan',
            phone_number='+375 (29) 123-45-67',
            email='sup@test.com'
        )

        self.department = Department.objects.create(
            name='Dept',
            location='Minsk'
        )

        self.user = User.objects.create_user(
            username='client',
            password='12345'
        )

        self.medicine = Medicine.objects.create(
            name='Ibuprofen',
            category=self.category,
            supplier=self.supplier,
            department=self.department,
            description='Desc',
            instruction='Instr',
            price=Decimal('10.00'),
            stock_quantity=100
        )

    def test_medicine_str(self):
        assert str(self.medicine) == 'Ibuprofen'

    def test_sale_item_cost(self):
        sale = Sale.objects.create(
            client=self.user,
            department=self.department
        )

        item = SaleItem.objects.create(
            sale=sale,
            medicine=self.medicine,
            quantity=2,
            price_at_sale=Decimal('10.00')
        )

        assert item.get_cost() == Decimal('20.00')

    def test_sale_total_amount(self):
        sale = Sale.objects.create(
            client=self.user,
            department=self.department
        )

        SaleItem.objects.create(
            sale=sale,
            medicine=self.medicine,
            quantity=3,
            price_at_sale=Decimal('10.00')
        )

        assert sale.total_amount == Decimal('30.00')


@pytest.mark.django_db
class TestCatalogViews:

    def setup_method(self):
        self.category = Category.objects.create(name='Tablets')

        self.supplier = Supplier.objects.create(
            name='Supplier',
            contact_person='Ivan',
            phone_number='+375 (29) 123-45-67',
            email='sup@test.com'
        )

        self.department = Department.objects.create(
            name='Dept',
            location='Minsk'
        )

        self.medicine = Medicine.objects.create(
            name='Ibuprofen',
            category=self.category,
            supplier=self.supplier,
            department=self.department,
            description='Desc',
            instruction='Instr',
            price=Decimal('10.00'),
            stock_quantity=100
        )

    def test_medicine_list(self, client):
        response = client.get(reverse('medicine_list'))

        assert response.status_code == 200

    def test_medicine_search(self, client):
        response = client.get(
            reverse('medicine_list'),
            {'search': 'Ibu'}
        )

        medicines = response.context['medicines']

        assert len(medicines) == 1

    def test_login_required_sale(self, client):
        response = client.get(reverse('sale_create'))

        assert response.status_code == 302


@pytest.mark.django_db
class TestStatisticsService:

    def test_empty_statistics(self):
        result = StatisticsService.get_sale_aggregations()

        assert result['mean'] == 0
        assert result['median'] == 0

    @patch('catalog.services.requests.get')
    def test_external_news_api_mock(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'articles': [{'title': 'Test'}]
        }

        from catalog.services import ExternalAPIService

        result = ExternalAPIService.get_medical_news()

        assert len(result) == 1

@pytest.mark.django_db
class TestStatisticsAdvanced:
    def setup_method(self):
        self.dept = Department.objects.create(name='Dept', location='Test')
        self.cat = Category.objects.create(name='Cat')
        self.sup = Supplier.objects.create(name='Sup', contact_person='C', phone_number='1', email='e@e.com')
        
        self.med = Medicine.objects.create(
            name='Med', 
            price=Decimal('100.00'), 
            stock_quantity=10, 
            category=self.cat, 
            department=self.dept, 
            supplier=self.sup
        )
        self.user = User.objects.create_user(username='test_client', role='client', date_of_birth='1990-01-01')
        self.sale = Sale.objects.create(client=self.user, department=self.dept)
        SaleItem.objects.create(sale=self.sale, medicine=self.med, quantity=2, price_at_sale=Decimal('100.00'))

    def test_get_total_revenue(self):
        result = StatisticsService.get_total_revenue()
        assert float(result['total_revenue']) == 200.0
        assert result['revenue_by_dept'][0]['dept_revenue'] == 200.0

    def test_get_product_insights(self):
        result = StatisticsService.get_product_insights()
        assert result['most_popular']['medicine__category__name'] == 'Cat'
        assert result['most_profitable']['total_profit'] == 200.0

    def test_get_client_age_stats(self):
        result = StatisticsService.get_client_age_stats()
        assert result['mean_age'] > 0

@pytest.mark.django_db
class TestSaleProcess:
    def test_sale_creation_reduces_stock(self, client):
        admin = User.objects.create_superuser(username='admin', password='123', email='a@a.com')
        client.login(username='admin', password='123')

        dept = Department.objects.create(name='Main', location='Minsk')
        cat = Category.objects.create(name='PillsCat')
        sup = Supplier.objects.create(name='PillsSup', email='p@p.com')
        
        med = Medicine.objects.create(
            name='Pills', 
            price=Decimal('10.00'), 
            stock_quantity=50, 
            department=dept, 
            category=cat, 
            supplier=sup
        )
        
        url = reverse('sale_create')

        data = {
            'department': dept.id,
            'client': admin.id,  
            'applied_promocode': '',

            'items-TOTAL_FORMS': '1',
            'items-INITIAL_FORMS': '0',
            'items-MIN_NUM_FORMS': '0',
            'items-MAX_NUM_FORMS': '1000',

            'items-0-medicine': med.id,
            'items-0-quantity': '5',
            'items-0-price_at_sale': '10.00',
        }
        
        response = client.post(url, data)

        if response.status_code == 200:
            print("\nОшибки основной формы:", response.context['form'].errors)
            print("Ошибки формсета:", response.context['items'].errors)

        assert response.status_code == 302
        
        med.refresh_from_db()
        assert med.stock_quantity == 45