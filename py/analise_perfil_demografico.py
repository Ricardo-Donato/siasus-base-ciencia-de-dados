import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from carrega_dados_view import carregar_dados
from preparacao_dados import preparar_dados

dados = carregar_dados()
if dados is None:
    raise SystemExit("Não foi possível carregar dbsia.pa_ijui; confira a conexão MySQL.")
df = preparar_dados(dados)
print("Linhas carregadas para análise:", len(df))

tabela = pd.crosstab(df["FAIXA_ETARIA"], df["PA_SEXO"])
print(tabela)

plt.figure(figsize=(8, 6))
sns.heatmap(tabela, annot=True, fmt="d", cmap="Blues")
plt.title("Atendimentos por faixa etaria e sexo")
plt.xlabel("Sexo")
plt.ylabel("Faixa etaria")
plt.tight_layout()
plt.savefig("grafico_heatmap_idade_sexo.png")
plt.show()
