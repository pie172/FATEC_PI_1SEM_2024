from pymongo import MongoClient

connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
db_connection = client["Connect_Food"]

print(db_connection)
print()
collection = db_connection.get_collection("doadores")

print(collection)
print()
search_filter = { "nome": "Jose" }
response = collection.find(search_filter)

for registry in response: print(registry)