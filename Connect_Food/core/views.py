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
            erros.append('Data de validade deve estar no formato DD-MM-YYYY.')

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


def saiba_mais(request):
    return render(request, 'saiba_mais.html')

#framework de aggregation

def resultados_agregados(request):
    manager = Doacao()
    
    # Consulta 1: Total de Alimentos por Categoria
    pipeline_categoria = [
        {"$group": {
            "_id": "$categoria",
            "total_alimentos": {"$sum": "$quantidade"}
        }},
        {"$sort": {"total_alimentos": -1}}
    ]
    total_alimentos_por_categoria = manager.executar_agregacao(pipeline_categoria)
    # Renomeando chave _id para categoria
    for item in total_alimentos_por_categoria:
        item['categoria'] = item.pop('_id')
    
    # Consulta 2: Doadores com Maior Quantidade de Doações
    pipeline_doadores = [
        {"$group": {
            "_id": "$nome",
            "total_doado": {"$sum": "$quantidade"}
        }},
        {"$sort": {"total_doado": -1}},
        {"$limit": 5}
    ]
    doadores_mais_doaram = manager.executar_agregacao(pipeline_doadores)
    # Renomeando chave _id para nome
    for item in doadores_mais_doaram:
        item['nome'] = item.pop('_id')
    
    # Consulta 3: Alimentos Próximos da Validade
    pipeline_validade = [
        {"$match": {
            "validade": {"$gte": datetime.now()}
        }},
        {"$sort": {"validade": 1}},
        {"$limit": 10}
    ]
    alimentos_proximos_validade = manager.executar_agregacao(pipeline_validade)
    
    # Consulta 4: Quantidade Total de Alimentos Disponíveis
    pipeline_quantidade_total = [
        {"$group": {
            "_id": None,
            "quantidade_total": {"$sum": "$quantidade"}
        }}
    ]
    quantidade_total_alimentos = manager.executar_agregacao(pipeline_quantidade_total)
    
    # Consulta 5: Histórico de Retiradas por Receptor
    pipeline_retiradas = [
        {"$match": {
            "nome_recebedor": {"$ne": None}
        }},
        {"$group": {
            "_id": "$nome_recebedor",
            "total_retirado": {"$sum": "$quantidade_retirou"}
        }},
        {"$sort": {"total_retirado": -1}}
    ]
    historico_retiradas_receptor = manager.executar_agregacao(pipeline_retiradas)
    # Renomeando chave _id para nome_recebedor
    for item in historico_retiradas_receptor:
        item['nome_recebedor'] = item.pop('_id')
    
    contexto = {
        'total_alimentos_por_categoria': total_alimentos_por_categoria,
        'doadores_mais_doaram': doadores_mais_doaram,
        'alimentos_proximos_validade': alimentos_proximos_validade,
        'quantidade_total_alimentos': quantidade_total_alimentos,
        'historico_retiradas_receptor': historico_retiradas_receptor
    }
    
    return render(request, 'relatorio.html', contexto)
