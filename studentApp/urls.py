from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('dashboard/', views.dashboard , name='dashboard'),
    path('add/', views.add , name='add'),
    path('view/', views.view , name='view'),
    path('collectfees/', views.collectfees , name='collectfees'),
    path('recipt/', views.recipt , name='recipt'),
    path('confirm/', views.confirm_person, name='confirm_person'),
    path('update/<int:id>/', views.update_person, name='update_person'),
    path('delete/<int:id>/', views.delete_person, name='delete_person'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
