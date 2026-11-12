import pandas as pd
import conexao as conexao

# Consulta SQL única para recuperar todas as colunas e linhas da VIEW.
def carregar_dados(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM dbsia.pa_ijui")
        return pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)

tabela = conexao.usar_conexao(carregar_dados)

# display está retornando undefined, ver com o professor
# display(tabela.head(10))
print(tabela.head(10))