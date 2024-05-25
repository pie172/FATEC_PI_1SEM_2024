from django.shortcuts import render
from .services import Doacao

# Create your views here.
def index(request):
    return render(request, 'index.html')

def doar_alimento(request):
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome'),
            'cpf': request.POST.get('cpf'),
            'cnpj': request.POST.get('cnpj'),
            'email': request.POST.get('email'),
            'alimento_id': int(request.POST.get('alimento_id')),
            'categoria': request.POST.get('categoria'),
            'alimento': request.POST.get('alimento'),
            'quantidade': int(request.POST.get('quantidade')),
            'validade': request.POST.get('validade')
        }
        manager = Doacao()
        manager.doar_alimento(**dados)
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
        manager.receber_alimentos(**dados)
    return render(request, 'receber_alimento.html')

def mostrar_alimentos(request):
    pass