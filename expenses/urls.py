from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-expense/', views.addExpense, name='add-expense'),
    path('edit-expense/<int:id>/', views.editExpense, name='edit'),
    path('delete-expense/<int:id>/', views.deleteExpense, name='delete'),
]
