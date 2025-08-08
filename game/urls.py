from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.play, name='play'),
    path('check-answer/', views.check_answer, name='check_answer'),
    path('results/', views.results, name='results'),
]