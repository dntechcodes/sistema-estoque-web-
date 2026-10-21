from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Categoria, Produto, Venda, ItemVenda
from decimal import Decimal

def produtos(request):
    """RF01 e RF02: Registo e listagem de produtos."""
    if request.method == 'POST':
        Produto.objects.create(
            nome=request.POST.get('nome'),
            categoria_id=request.POST.get('categoria_id'),
            preco=Decimal(request.POST.get('preco').replace(',', '.')),
            estoque_atual=int(request.POST.get('estoque_atual')),
            estoque_minimo=int(request.POST.get('estoque_minimo'))
        )
        messages.success(request, 'Produto registado com sucesso!')
        return redirect('produtos')
        
    lista_produtos = Produto.objects.all()
    lista_categorias = Categoria.objects.all()
    return render(request, 'estoque/produtos.html', {'produtos': lista_produtos, 'categorias': lista_categorias})

def categorias(request):
    """RF06: Registo e listagem de categorias."""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            Categoria.objects.create(nome=nome)
            messages.success(request, 'Categoria registada com sucesso!')
        return redirect('categorias')
    
    lista_categorias = Categoria.objects.all()
    return render(request, 'estoque/categorias.html', {'categorias': lista_categorias})

@transaction.atomic
def nova_venda(request):
    """RF04: Registo de saída com baixa transacional e atómica de estoque."""
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade'))
        
        produto = get_object_or_404(Produto, id=produto_id)
        
        if produto.estoque_atual < quantidade:
            messages.error(request, f'Erro: Estoque insuficiente para {produto.nome}.')
            return redirect('nova_venda')
            
        venda = Venda.objects.create()
        item = ItemVenda.objects.create(
            venda=venda, produto=produto, quantidade=quantidade, preco_unitario=produto.preco
        )
        venda.valor_total = item.subtotal()
        venda.save()
        
        produto.estoque_atual -= quantidade
        produto.save()
        
        messages.success(request, 'Venda registada e estoque atualizado!')
        return redirect('estoque_baixo') 
        
    lista_produtos = Produto.objects.all()
    return render(request, 'estoque/nova_venda.html', {'produtos': lista_produtos})

def estoque_baixo(request):
    """RF05: Lista produtos abaixo ou no limite do estoque mínimo."""
    todos_produtos = Produto.objects.all()
    produtos_alerta = [p for p in todos_produtos if p.verificar_estoque_baixo()]
    return render(request, 'estoque/estoque_baixo.html', {'produtos': produtos_alerta})

# Create your views here.
