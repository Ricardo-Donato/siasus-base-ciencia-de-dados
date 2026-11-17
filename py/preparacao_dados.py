import pandas as pd

def preparar_dados(df):
    df = df.copy()

    # A view usa nomes de colunas do esquema analítico; estes aliases mantêm
    # compatibilidade com os scripts que foram escritos para os campos PARS.
    aliases = {
        "PA_SEXO": "pa_sexo",
        "PA_IDADE": "pa_idade",
        "PA_FLIDADE": "pa_flidade",
        "PA_CIDPRI": "pa_cidpri",
        "PA_QTDPRO": "pa_qtdpro",
        "PA_QTDAPR": "pa_qtdapr",
        "PA_VALPRO": "pa_valpro",
        "PA_VALAPR": "pa_valapr",
    }
    for destino, origem in aliases.items():
        if destino not in df.columns and origem in df.columns:
            df[destino] = df[origem]

    # As linhas idênticas na view não são removidas: sem chave de origem não
    # é possível afirmar que sejam duplicações indevidas do PARS.
    for col in ["PA_IDADE", "PA_QTDPRO", "PA_QTDAPR", "PA_VALPRO", "PA_VALAPR"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "PA_PROC_ID" in df.columns:
        df["PA_PROC_ID"] = df["PA_PROC_ID"].fillna("").astype("string").str.zfill(10)
    if "PA_TPUPS" in df.columns:
        df["PA_TPUPS"] = df["PA_TPUPS"].fillna("").astype("string").str.zfill(2)

    # PA_FLIDADE é um indicador de compatibilidade da idade com a faixa etária
    # prevista para o procedimento; não é unidade de medida da idade.
    if "PA_IDADE" in df.columns:
        idade_valida = df["PA_IDADE"].between(0, 120)
        faixas = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 121]
        nomes = ["0-4", "5-9", "10-14", "15-19", "20-29", "30-39",
                 "40-49", "50-59", "60-69", "70-79", "80+"]
        df["FAIXA_ETARIA"] = pd.cut(
            df["PA_IDADE"].where(idade_valida),
            bins=faixas,
            labels=nomes,
            right=False,
        )

    return df
