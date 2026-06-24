from django.urls import path
from .views import ValidateFoodView

urlpatterns = [
    path('validar/', ValidateFoodView.as_view(), name='validar_comida')
]