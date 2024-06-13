from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from datetime import datetime


class Doacao():
    def __init__(self, db_name='connect_food', uri='mongodb://localhost:27017/'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['doadores']
        # Verificando se duplicidade no id do alimento
        self.collection.create_index([("alimento_id", ASCENDING)], unique=True)

    def doar_alimento(self, **kwargs):
        documento = {
            "nome": kwargs.get('nome'),
            "cpf": kwargs.get('cpf') if kwargs.get('cpf') else None,
            "cnpj": kwargs.get('cnpj') if kwargs.get('cnpj') else None,
            "email": kwargs.get('email'),
            "telefone": kwargs.get('telefone'),
            "endereco": kwargs.get('endereco'),
            "horario": kwargs.get('horario'),
            "alimento_id": kwargs.get('alimento_id'),
            "categoria": kwargs.get('categoria'),
            "alimento": kwargs.get('alimento'),
            "quantidade": kwargs.get('quantidade'),
            "quant_medida": kwargs.get('quantidade'),
            "validade": datetime.strptime(kwargs.get('validade'), '%Y-%m-%d') if kwargs.get('validade') else None,
            "nome_recebedor": None,
            "quantidade_retirou": None,
            "cnpj_recebedor": None,
            "email_recebedor": None
        }
        try:
            result = self.collection.insert_one(documento)
            return {'inserted_id': str(result.inserted_id)}
        except DuplicateKeyError as e:
            return {'error': 'Erro: Código do alimento já existe. Por favor, forneça um código único.'}


    def receber_alimentos(self, **kwargs):
        filtro = {"alimento_id": kwargs.get('alimento_id')}
        documento = self.collection.find_one(filtro)
        
        if not documento:
            return {'error': 'Erro Alimento não encontrado'}
        
        quant_atualizada = documento['quantidade'] - kwargs.get('quantidade_retirou')
        if quant_atualizada < 0:
            return {'error': 'Erro Quantidade retirada maior que a disponível.'}
        
        atualizacao = {
            "$set": {
                "nome_recebedor": kwargs.get('nome_recebedor'),
                "quantidade_retirou": kwargs.get('quantidade_retirou'),
                "cnpj_recebedor": kwargs.get('cnpj_recebedor'),
                "email_recebedor": kwargs.get('email_recebedor'),
                "quantidade": quant_atualizada
            }
        }
        if quant_atualizada == 0:
            self.collection.delete_one(filtro)
        else:
            self.collection.update_one(filtro, atualizacao)
            
        return {'modified_count': 1}

    def listar_alimentos(self):
        alimentos = self.collection.find({}, {
            "alimento_id": 1,
            "categoria": 1,
            "alimento": 1,
            "quantidade": 1,
            "quant_medida": 1,
            "validade": 1
        })
        return list(alimentos)
    
    def buscar_por_id(self, alimento_id):
        documento = self.collection.find_one({"alimento_id": alimento_id})
        return documento if documento else None

    #framework de aggregation
    def executar_agregacao(self, pipeline):
        return list(self.collection.aggregate(pipeline))