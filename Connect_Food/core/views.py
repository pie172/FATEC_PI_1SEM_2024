from django.shortcuts import render
from .services import Doacao
from django.http import JsonResponse

def index(request):
    manager = Doacao()
    alimentos = manager.listar_alimentos()
    return render(request, 'index.html', {'alimentos': alimentos})

def doar_alimento(request):
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome'),
            'cpf': request.POST.get('cpf'),
            'cnpj': request.POST.get('cnpj'),
            'email': request.POST.get('email'),
            "telefone": request.POST.get('telefone'),
            "endereco": request.POST.get('endereco'),
            "horario": request.POST.get('horario'),
            'alimento_id': int(request.POST.get('alimento_id')),
            'categoria': request.POST.get('categoria'),
            'alimento': request.POST.get('alimento'),
            'quantidade': int(request.POST.get('quantidade')),
            'validade': request.POST.get('validade')
        }
        manager = Doacao()
        result = manager.doar_alimento(**dados)
        # Verificando se duplicidade no id do alimento, se já estiver no banco dá erro e aperece uma mensagem
        if 'error' in result:
            return render(request, 'doar_alimento.html', {'error': result['error']})
        else:
            return render(request, 'doar_alimento.html', {'success': 'Doação realizada com sucesso!'})
    return render(request, 'doar_alimento.html')

def receber_alimento(request):
    if request.method == 'POST':
        dados = {
            'alimento_id': int(request.POST.get('alimento_id')),
            'nome_recebedor': request.POST.get('nome_recebedor'),
            'quantidade_retirou': int(request.POST.get('quantidade_retirou')),
            'cnpj_recebedor': request.POST.get('cnpj_recebedor'),
            'email_recebedor': request.POST.get('email_recebedor')
        }
        manager = Doacao()
        result = manager.receber_alimentos(**dados)
        if 'error' in result:
            return render(request, 'receber_alimento.html', {'error': result['error']})
        else:
            return render(request, 'receber_alimento.html', {'success': 'Alimento recebido com sucesso!'})
    return render(request, 'receber_alimento.html')