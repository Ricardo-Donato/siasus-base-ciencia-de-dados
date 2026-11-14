Manipulação de Banco de Dados  NoSQL em Python 
Disciplina: Programação para Ciência de Dados
MongoDB: Orientado a  Documento 
Documentação oficial  
https://docs.mongodb.com/manual
Modelo de Dados: MySQL vs. MongoDB 
● Arquitetura MongoDB 
○ Uma instância pode conter vários databases. 
○ Um database possui várias coleções. 
○ Cada coleção armazena múltiplos documentos. 
● Documentos MongoDB 
○ Conjunto não ordenado de pares chave-valor. 
○ Sem esquema rígido: cada documento pode ter diferentes atributos.
Relacional vs. Orientado a Documento Coleção: Pessoa 

Colunas Tabela: Pessoa Linhas 
documento documento documento 
id Nome Tel 
1 Anna 3381-2800 { "_id": 1,  "nome": "Anna", 
 "tel": "3381-2800" 
} 
{ 
 "_id": 2, 
 "nome": "Pedro", 
 "tel": "3381-2801" 
} 
Coleção: Pessoa

Configuração do Ambiente do MongoDB Baixar e instalar o MongoDB Community Server: https://fastdl.mongodb.org/windows/mongodb-windows-x86 _64-9.0.2-signed.msi 
Baixar e instalar o MongoDB Compass (GUI): https://downloads.mongodb.com/compass/mongodb-compa ss-1.52.0-win32-x64.exe

Criar o DBVEN e as Coleções

Importar os Dados para as Coleções

Manipulando Dados no MongoDB Compass
MongoDB Shell: Comandos Básicos 
# Listando os bancos de dados 
show dbs 
# Listando as coleções 
use dbven 
show collections 
# Adicionando um documento em uma coleção chamada clientes db.clientes.insertOne({ _id: 13, cliente: "Juca", estado: "RS", sexo: "M", status: "Silver"}) 
# Listando a quantidade de documentos em uma coleção chamada clientes 
db.clientes.countDocuments() 
# Obtendo os documentos contidos em uma coleção chamada clientes db.clientes.find() 
# Obtendo um documento por meio de seu id 
db.clientes.find({ _id: 10}) 
# Obtendo um documento pelo valor associado a chave 'cliente' db.clientes.find({ cliente: "Alexandra Tabares" })
Comparando Instruções: SQL vs MongoDB 

● Criando e inserindo  dados: 
SQL: 
CREATE TABLE pessoa ( 
 idPessoa INT NOT NULL AUTO_INCREMENT,  nome VARCHAR(40), 
 email VARCHAR(40), 
 PRIMARY KEY (idPessoa) 
); 
MongoDB: 
● Alterando Estrutura /  Atualizando  
Documentos: 
SQL: 
ALTER TABLE pessoa ADD data DATETIME; ALTER TABLE pessoa DROP COLUMN data; 
db.pessoas.insertOne({  nome: "Juca", 
 email: "juca@email.com" }); 
MongoDB: 
db.pessoas.updateMany({}, { $set: { data: new Date() } }); db.pessoas.updateMany({}, { $unset: { data: "" } });

Inserção de Documentos no MongoDB 

● Inserindo um único  documento: 
db.empregados.insertOne({ 
 CdEmp: 5, 
 NmEmp: "Paulo", 
 Salario: 500.0, 
 DtNasc: ISODate("1987-03-02T00:00:00Z"),  CdCidade: 100 
}); 
● Inserindo múltiplos  documentos: 
db.empregados.insertMany([ 
 { 
 CdEmp: 1, 
 NmEmp: "Maria", 
 Salario: 100.0, 
 DtNasc: ISODate("1979-11-10T00:00:00Z"),  CdCidade: 100 
 }, 
 { 
 CdEmp: 2, 
 NmEmp: "João", 
 Salario: 120.0, 
 DtNasc: ISODate("1986-08-15T00:00:00Z"),  CdCidade: 1000 
 } 
]); 

https://www.mongodb.com/pt-br/docs/manual/tutorial/insert-documents/
Consulta de Documentos no MongoDB ● Recuperando todos os documentos da coleção empregados: db.empregados.find({}); 
● Recuperando um documento específico: 
db.empregados.find({ NmEmp: "Maria" }); 
● Usando operadores lógicos AND e OR: 
// Recuperando empregados chamados "Maria" AND com salário menor que 500 db.empregados.find({ NmEmp: "Maria", Salario: { $lt: 500 } }); 
// Recuperando empregados chamados "Maria" OU com salário maior que 500 db.empregados.find({ $or: [ { NmEmp: "Maria" }, { Salario: { $gt: 500 } } ] }); 
https://www.mongodb.com/pt-br/docs/manual/tutorial/query-documents/
Atualização de Documentos no MongoDB ● Métodos para atualização: 
db.collection.updateOne(<filter>, <update>, <options>); 
db.collection.updateMany(<filter>, <update>, <options>); 
● Exemplo: atualizando um único documento na coleção  empregados: 
db.empregados.updateOne( 
 { NmEmp: "Maria" }, 
 { $set: { Salario: 200.0 } } 
); 
https://www.mongodb.com/pt-br/docs/manual/tutorial/update-documents/
Exclusão de Documentos no MongoDB ● Métodos para exclusão: 
db.collection.deleteOne(<filter>); 
db.collection.deleteMany(<filter>); 
● Exemplo: excluindo um único documento na coleção  empregados: 
db.empregados.deleteOne({ Salario: 100.0 }); 
https://www.mongodb.com/pt-br/docs/manual/tutorial/remove-documents/
MongoDB — Consultas & Junções 
Manual oficial:  
https://www.mongodb.com/pt-br/docs/manual/  Junção entre coleções com $lookup (similar ao JOIN): https://www.mongodb.com/pt-br/docs/manual/reference/op erator/aggregation/lookup/ 
db.vendas.aggregate([ 
 { $lookup: { 
 from: "clientes", 
 localField: "idCliente", 
 foreignField: "_id", 
 as: "cliente" 
 }}, 
 { $unwind: "$cliente" }, 
 { $project: { _id: 1, data: 1, total: 1, "cliente.cliente": 1 } } ])
MongoDB — Filtros / ordenação / limite  (WHERE + ORDER BY + LIMIT) 
$gt:  
https://www.mongodb.com/docs/manual/reference/operator /query/gt/ 
$lt:  
https://www.mongodb.com/docs/manual/reference/operator /query/lt/ 
// Vendas com total > 10.000, ordenadas desc, top 10 
// $gt (“greater than”) é o operador de comparação “maior que” do MongoDB. 
db.vendas.find({ total: { $gt: 10000 } }, { _id: 1, data: 1, total: 1 })  .sort({ total: -1 }) 
 .limit(10)
Filtro por texto com $regex (atenção a  índices/opções) 
$regex: :  
https://www.mongodb.com/pt-br/docs/manual/reference/op erator/query/regex/ 
// Clientes cujo nome começa com “A”, case-insensitive db.clientes.find({ cliente: { $regex: "^A", $options: "i" } })
Conector Python com MongoDB PyMongo: Instalar o pacote pymongo com o pip: 
pip install pymongo
Criar uma Conexão com Pymongo Abrir conexão e entregar db à função-alvo. 
from pymongo import MongoClient 
def usar_conexao_mongo(acao, uri="mongodb://localhost:27017", dbname="dbven"):  with MongoClient(uri) as client:  
 db = client[dbname] 
 print(f"Conectado a {uri} / db={dbname}") 
 return acao(db)
Centralização das credenciais/URIs aqui; o resto da  aplicação só recebe db. 
Consultas Básicas 
Listar bancos e coleções do dbven. 
from conexao_mongo import usar_conexao_mongo 
def listar(db): 
 print("Databases:", db.client.list_database_names())  print("Coleções em dbven:", db.list_collection_names()) 
usar_conexao_mongo(listar)
SELECT * ... LIMIT 5 (várias coleções) Projetar até 5 documentos por coleção. 
from conexao_mongo import usar_conexao_mongo 
def selecionar(db): 
 colecoes = ["vendedores", "produtos", "clientes", "vendas", "itensvenda"] 
 for col in colecoes: 
 print(f"\n---- {col} (5 documentos) ----") 
 cursor = db[col].find({}).limit(5) 
 docs = list(cursor) 
 if not docs: 
 print("(sem documentos)") 
 else: 
 for d in docs: 
 print(d) 
usar_conexao_mongo(selecionar)
WHERE + ORDER BY + LIMIT 
Filtrar e ordenar (vendas e produtos). 
from conexao_mongo import usar_conexao_mongo 
def consultar(db): 
 # Vendas total > 10000 (top 10) 
 for v in (db.vendas.find({"total": {"$gt": 10000}}, {"_id":1,"data":1,"total":1})  .sort([("total",-1)]).limit(10)): 
 print((v["_id"], v["data"], v["total"])) 
 # Produtos preço > 100 (top 10) 
 for p in (db.produtos.find({"preco": {"$gt": 100}}, {"_id":1,"produto":1,"preco":1})  .sort([("preco",-1)]).limit(10)): 
 print((p["_id"], p["produto"], p["preco"])) 
usar_conexao_mongo(consultar)
{"campo": {"$gt": valor}} ⇔ WHERE campo > valor 
INSERT (vendedores) 
Inserir um novo documento na coleção Vendedores. 
from conexao_mongo import usar_conexao_mongo 
from pymongo.errors import DuplicateKeyError 
def inserir(db): 
 try: 
 db.vendedores.insert_one({"_id": 13, "nome": "Luciana Cardoso"})  print("Vendedor inserido.") 
 except DuplicateKeyError: 
 print("ID já existente.") 
usar_conexao_mongo(inserir)
Mongo não tem commit para insert_one: a escrita já é  confirmada na operação. 
UPDATE (clientes → Status = Gold) Atualizar status do cliente _id = 1. 
from conexao_mongo import usar_conexao_mongo 
def atualizar_status_cliente(db): 
 res = db.clientes.update_one({"_id": 1}, {"$set": {"status": "Gold"}}) 
 print("Docs Afetados:", res.matched_count, "DocsModificados:", res.modified_count) 
usar_conexao_mongo(atualizar_status_cliente)
