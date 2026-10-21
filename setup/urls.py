from django.contrib import admin
from django.urls import path
from estoque import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # As 4 rotas exatas do sistema
    path('', views.produtos, name='produtos'), 
    path('categorias/', views.categorias, name='categorias'),
    path('nova-venda/', views.nova_venda, name='nova_venda'),
    path('estoque-baixo/', views.estoque_baixo, name='estoque_baixo'),
]
