from django.shortcuts import render
from .services import Doacao
import re
from datetime import datetime

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
        
        # Validações
        erros = []

        # Validação de CPF (11 dígitos numéricos)
        if dados['cpf'] and not re.match(r'^\d{11}$', dados['cpf']):
            erros.append('CPF deve ter 11 dígitos numéricos.')
        
        # Validação de CNPJ (14 dígitos numéricos)
        if dados['cnpj'] and not re.match(r'^\d{14}$', dados['cnpj']):
            erros.append('CNPJ deve ter 14 dígitos numéricos.')

        # Validação de telefone (aceitando formatos diferentes, mas apenas números)
        if not re.match(r'^\(?\d{2}\)?\d{4,5}-?\d{4}$', dados['telefone']):
            erros.append('Telefone deve ter o formato correto (ex: (11) 99999-9999 ou 11999999999).')
        
        # Validação de validade
        try:
            validade = datetime.strptime(dados['validade'], '%Y-%m-%d')
            if validade < datetime.now():
                erros.append('Data de validade deve ser no mínimo a data atual.')
        except ValueError:
            erros.append('Data de validade deve estar no formato YYYY-MM-DD.')

        # Se houver erros, renderiza o template com os erros e os dados preenchidos
        if erros:
            return render(request, 'doar_alimento.html', {'error': ' '.join(erros), 'data': dados})
        
        manager = Doacao()
        result = manager.doar_alimento(**dados)
        # Verificando se duplicidade no id do alimento, se já estiver no banco dá erro e aperece uma mensagem
        if 'error' in result:
            return render(request, 'doar_alimento.html', {'error': result['error'], 'data': dados})
        else:
            return render(request, 'doar_alimento.html', {'success': 'Doação realizada com sucesso!', 'data': {}})
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
            
            erros = []
            
            # Validação de CNPJ (14 dígitos numéricos)
            if dados['cnpj_recebedor'] and not re.match(r'^\d{14}$', dados['cnpj_recebedor']):
                erros.append('CNPJ deve ter 14 dígitos numéricos.')
            if erros:
                return render(request, 'receber_alimento.html', {'error': ' '.join(erros), 'data': dados})
                
            result = manager.receber_alimentos(**dados)
            if 'error' in result:
                return render(request, 'receber_alimento.html', {'error': result['error'], 'data': dados})
            else:
                return render(request, 'receber_alimento.html', {'success': 'Alimento recebido com sucesso!', 'data': {}})
    
    return render(request, 'receber_alimento.html', {'doacao': doacao})
