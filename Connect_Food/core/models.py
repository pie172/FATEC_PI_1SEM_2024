from pymongo import MongoClient
import datetime
import pprint

# Conectando ao MongoDB
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db_connection = client["Connect_Food"] 

print(db_connection)
print()
collection = db_connection.get_collection("doadores")

print(collection)
print()
response = collection.find()

for registry in response: 
    print(registry)


nome = input("Em qual nome será cadastrado? \n")
cpf = input("CPF: \n")
cnpj= input("CNPJ: \n")
categoria= input("Categoria: \n")
alimento = input("Alimento: \n")
quantidade = input("Quantidade: \n")


post = {
  "nome": nome,
  "cpf": cpf,
  "cnpj": cnpj,
  "categoria": categoria,
  "alimento": alimento,
  "quantidade": quantidade,
  "data": datetime.datetime.now()  
}

collection.insert_one(post)


collection = db_connection.get_collection("doadores")
