import pandas as pd
import matplotlib.pyplot as plt

from carrega_dados_view import carregar_dados
from preparacao_dados import preparar_dados

dados = carregar_dados()
if dados is None:
    raise SystemExit("Não foi possível carregar dbsia.pa_ijui; confira a conexão MySQL.")
df = preparar_dados(dados)

oncologia = df[df["PA_PROC_ID"].str.startswith("0304")]

saude_mental = df[df["PA_CIDPRI"].str.startswith("F", na=False) | (df["PA_TPUPS"] == "70")]

atencao_basica = df[df["PA_TPUPS"].isin(["01", "02"])]

areas = {"Oncologia": oncologia,
         "Saude mental": saude_mental,
         "Atencao basica": atencao_basica}

resumo = pd.DataFrame({
    nome: {
        "qtd_apresentada": a["PA_QTDPRO"].sum(),
        "qtd_aprovada": a["PA_QTDAPR"].sum(),
        "valor_apresentado": a["PA_VALPRO"].sum(),
        "valor_aprovado": a["PA_VALAPR"].sum(),
    } for nome, a in areas.items()
}).T
print(resumo)
resumo.to_csv("resumo_areas_criticas.csv")

fig, eixos = plt.subplots(1, 2, figsize=(12, 5))
resumo[["qtd_apresentada", "qtd_aprovada"]].plot(kind="bar", ax=eixos[0])
eixos[0].set_title("Quantidade")
resumo[["valor_apresentado", "valor_aprovado"]].plot(kind="bar", ax=eixos[1])
eixos[1].set_title("Valor (R$)")
for e in eixos:
    e.tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig("grafico_areas_apresentado_vs_aprovado.png")
plt.show()
