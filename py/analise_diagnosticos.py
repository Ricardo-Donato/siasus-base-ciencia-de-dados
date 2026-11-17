import matplotlib.pyplot as plt

from carrega_dados_view import carregar_dados
from preparacao_dados import preparar_dados

dados = carregar_dados()
if dados is None:
    raise SystemExit("Não foi possível carregar dbsia.pa_ijui; confira a conexão MySQL.")
df = preparar_dados(dados)

cid = df["PA_CIDPRI"].astype("string").str.strip()
diagnostico = df["Diagnostico"].astype("string").str.strip()
diagnostico_normalizado = diagnostico.str.upper()
cid_especial = (
    cid.isna()
    | cid.isin(["", "0000", "9999"])
    | diagnostico_normalizado.isin(
        ["CID NAO INFORMADO", "CID NÃO INFORMADO", "CID NÃO IDENTIFICADO", "CID INVALIDO"]
    )
)
print("Registros sem diagnóstico CID utilizável:", int(cid_especial.sum()), "de", len(df))

dados_validos = df.loc[~cid_especial & diagnostico.notna()]
top_diagnosticos = dados_validos["Diagnostico"].value_counts().head(10)
print("CID informado por descrição do diagnóstico:")
print(top_diagnosticos)

plt.figure(figsize=(8, 6))
top_diagnosticos.sort_values().plot(kind="barh", color="steelblue")
plt.title("10 diagnósticos mais frequentes (CID informado)")
plt.xlabel("Quantidade de registros")
plt.ylabel("Diagnóstico")
plt.tight_layout()
plt.savefig("grafico_top10_cid.png")
plt.show()
