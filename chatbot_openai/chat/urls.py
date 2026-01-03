from django.urls import path
from .views import HolaMundoView

app_name = 'chat'

urlpatterns = [
    path('', HolaMundoView.as_view(), name='hola_mundo'),
]
