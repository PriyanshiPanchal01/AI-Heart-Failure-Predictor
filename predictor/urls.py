from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # urls.py mein urlpatterns list ke andar ye line dalein:
path('download-report/', views.generate_report, name='download_report'),
]