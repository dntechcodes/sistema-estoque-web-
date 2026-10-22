from django.contrib import admin
from django.urls import path
from estoque import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('', views.produtos, name='produtos'), 
    path('categorias/', views.categorias, name='categorias'),
    path('nova-venda/', views.nova_venda, name='nova_venda'),
    path('estoque-baixo/', views.estoque_baixo, name='estoque_baixo'),
    
    path('produto/editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('produto/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
]