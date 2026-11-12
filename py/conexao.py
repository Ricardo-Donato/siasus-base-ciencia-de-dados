# conexao.py
from getpass import getpass
from mysql.connector import connect, Error

def usar_conexao(acao):
    try:
        with connect(
            host="localhost",               # Endereço do servidor MySQL (localhost)
            user=input("Usuário: "),        # Solicita ao usuário o nome de login
            password=getpass("Senha: ")     # Solicita a senha de forma oculta
        ) as connection:
            print("Conexão estabelecida:", connection)
            return acao(connection)
    except Error as e:
        print("Ocorreu um erro ao conectar com o BD: ", e)