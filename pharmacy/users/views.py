import logging
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ClientRegistrationForm

logger = logging.getLogger('main')

class ClientRegistrationView(CreateView):
    form_class = ClientRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Новый пользователь зарегистрирован: {self.object.username} (ID: {self.object.id})")
        return response