from django.shortcuts import render
from .services import Doacao


def index(request):
    manager = Doacao()
    alimentos = manager.listar_alimentos()
    doador = None
    
    if request.method == 'POST':
        alimento_id = int(request.POST.get('alimento_id'))
        doador = manager.buscar_por_id(alimento_id)
    
    return render(request, 'index.html', {'alimentos': alimentos, 'doador': doador})

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
            'quant_medida': request.POST.get('quant_medida'),
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
    manager = Doacao()
    doacao = None
    
    if request.method == 'POST':
        # Verificando se estamos buscando por alimento_id ou recebendo o alimento
        if 'buscar' in request.POST:
            alimento_id = int(request.POST.get('alimento_id'))
            doacao = manager.buscar_por_id(alimento_id)
            if not doacao:
                return render(request, 'receber_alimento.html', {'error': 'Alimento não encontrado'})
        else:
            dados = {
                'alimento_id': int(request.POST.get('alimento_id')),
                'nome_recebedor': request.POST.get('nome_recebedor'),
                'quantidade_retirou': int(request.POST.get('quantidade_retirou')),
                'cnpj_recebedor': request.POST.get('cnpj_recebedor'),
                'email_recebedor': request.POST.get('email_recebedor')
            }
            result = manager.receber_alimentos(**dados)
            if 'error' in result:
                return render(request, 'receber_alimento.html', {'error': result['error']})
            else:
                return render(request, 'receber_alimento.html', {'success': 'Alimento recebido com sucesso!'})
    
    return render(request, 'receber_alimento.html', {'doacao': doacao})