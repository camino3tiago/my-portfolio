from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='top'),
    path('about/<int:pk>/', views.AboutMeView.as_view(), name='about'),
    path('services/', views.ServiceView.as_view(), name='services')
]
