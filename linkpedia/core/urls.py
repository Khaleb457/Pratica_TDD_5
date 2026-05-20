from django.urls import path
from core.views import login, logout, home, cadastro, listar


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('index/cadastro/', cadastro, name='cadastro'),
    path('index/listar/', listar, name='listar'),


    path('', home,name='home')
]