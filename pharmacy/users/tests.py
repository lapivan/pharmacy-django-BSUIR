import pytest
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse
from users.models import User
from users.forms import ClientRegistrationForm


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(
            username='ivan',
            password='test12345',
            role='client'
        )

        assert user.username == 'ivan'
        assert user.role == 'client'

    def test_user_str(self):
        user = User.objects.create_user(
            username='ivan',
            password='test12345',
            role='client'
        )

        assert str(user) == 'ivan (Client)'

    def test_underage_user_validation(self):
        user = User(
            username='young',
            date_of_birth=date.today()
        )

        with pytest.raises(ValidationError):
            user.clean()

    def test_valid_phone(self):
        user = User.objects.create_user(
            username='phoneuser',
            password='test12345',
            phone_number='+375 (29) 123-45-67'
        )

        assert user.phone_number == '+375 (29) 123-45-67'


@pytest.mark.django_db
class TestRegistrationForm:

    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'test@test.com',
            'phone_number': '+375 (29) 123-45-67',
            'date_of_birth': '2000-01-01',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }

        form = ClientRegistrationForm(data=form_data)

        assert form.is_valid()

    def test_registration_form_save_sets_client_role(self):
        form_data = {
            'username': 'newuser',
            'email': 'test@test.com',
            'phone_number': '+375 (29) 123-45-67',
            'date_of_birth': '2000-01-01',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        }

        form = ClientRegistrationForm(data=form_data)

        assert form.is_valid()

        user = form.save()

        assert user.role == 'client'


@pytest.mark.django_db
class TestViews:

    def test_register_page_get(self, client):
        response = client.get(reverse('register'))

        assert response.status_code == 200

    def test_register_post(self, client):
        response = client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@test.com',
            'phone_number': '+375 (29) 123-45-67',
            'date_of_birth': '2000-01-01',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
        })

        assert response.status_code == 302
        assert User.objects.filter(username='testuser').exists()