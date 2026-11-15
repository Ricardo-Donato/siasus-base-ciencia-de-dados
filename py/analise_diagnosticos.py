import matplotlib.pyplot as plt

from carrega_dados_view import carregar_dados
from preparacao_dados import preparar_dados

df = preparar_dados(carregar_dados())

print("CID vazio:", df["PA_CIDPRI"].isnull().sum(), "de", len(df))

top_cid = df["PA_CIDPRI"].value_counts().head(10)
print(top_cid)

plt.figure(figsize=(8, 6))
top_cid.sort_values().plot(kind="barh", color="steelblue")
plt.title("10 diagnosticos (CID-10) mais frequentes")
plt.xlabel("Quantidade de registros")
plt.ylabel("CID")
plt.tight_layout()
plt.savefig("grafico_top10_cid.png")
plt.show()
