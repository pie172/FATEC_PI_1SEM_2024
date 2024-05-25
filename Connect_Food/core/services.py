from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

class Doacao():
    def __init__(self, db_name='connect_food', uri='mongodb://localhost:27017/'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db['doadores']

    def doar_alimento(self, **kwargs):
        documento = {
            "nome": kwargs.get('nome'),
            "cpf": kwargs.get('cpf'),
            "cnpj": kwargs.get('cnpj') if kwargs.get('validade') else None,
            "email": kwargs.get('email') if kwargs.get('validade') else None,
            "alimento_id": kwargs.get('alimento_id'),
            "categoria": kwargs.get('categoria'),
            "alimento": kwargs.get('alimento'),
            "quantidade": kwargs.get('quantidade'),
            "validade": datetime.strptime(kwargs.get('validade'), '%Y-%m-%d') if kwargs.get('validade') else None,
            "nome_recebedor": None,
            "quantidade_retirou": None,
            "cnpj_recebedor": None,
            "email_recebedor": None
        }
        result = self.collection.insert_one(documento)
        return result.inserted_id

    def receber_alimentos(self, **kwargs):
        filtro = {"alimento_id": kwargs.get('alimento_id')}
        atualizacao = {
            "$set": {
                "nome_recebedor": kwargs.get('nome_recebedor'),
                "quantidade_retirou": kwargs.get('quantidade_retirou'),
                "cnpj_recebedor": kwargs.get('cnpj_recebedor'),
                "email_recebedor": kwargs.get('email_recebedor')
            }
        }
        result = self.collection.update_one(filtro, atualizacao)
        return result.modified_count
