import pandas as pd
import conexao

def _consultar_view(connection):
    """Consulta a view usando uma conexão já aberta."""
    with connection.cursor(buffered=True) as cursor:
        cursor.execute("SELECT * FROM dbsia.pa_ijui")
        colunas = cursor.column_names
        registros = cursor.fetchall()
    return pd.DataFrame(registros, columns=colunas)


def carregar_dados(connection=None):
    """Retorna a view; aceita conexão existente ou solicita uma conexão local."""
    if connection is not None:
        return _consultar_view(connection)
    return conexao.usar_conexao(_consultar_view)


if __name__ == "__main__":
    tabela = carregar_dados()
    if tabela is not None:
        print(tabela.head(10))
