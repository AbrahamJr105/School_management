from django.urls import path
from . import views
urlpatterns = [
    path('etudiant/', views.etudiant_form, name='etudiant'),
    path('enseignant/', views.enseignant_form, name='enseignant'),
    path('bulletin/',views.bulletin_view, name='bulletin'),
    path("", views.menu, name='menu'),
    path('statistique/', views.statistique, name='statistique'),
    path('pv', views.pv, name='pv'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('save-chart-image/', views.save_chart_image, name='save_chart_image'),
]