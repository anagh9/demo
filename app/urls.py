from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<expense_id>/',
         views.delete_expense, name='delete_expense'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
