from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cadastrar/', views.CadastrarConta.as_view(), name='cadastrar'),
    path('produtos/search/', views.SearchView.as_view(), name='search'),
    path('categoria/<int:id>', views.CategoriaView.as_view(), name='categoria'),
]
