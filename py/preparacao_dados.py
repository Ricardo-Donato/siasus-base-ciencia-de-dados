import pandas as pd

def preparar_dados(df):
    df = df.copy()

    df = df.drop_duplicates()

    for col in ["PA_IDADE", "PA_QTDPRO", "PA_QTDAPR", "PA_VALPRO", "PA_VALAPR"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["PA_PROC_ID"] = df["PA_PROC_ID"].fillna("").astype(str).str.zfill(10)
    df["PA_TPUPS"] = df["PA_TPUPS"].fillna("").astype(str).str.zfill(2)

    df = df[df["PA_IDADE"] <= 120]
    df = df[df["PA_SEXO"].isin(["M", "F"])]

    faixas = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 200]
    nomes = ["0-4", "5-9", "10-14", "15-19", "20-29", "30-39",
             "40-49", "50-59", "60-69", "70-79", "80+"]
    df["FAIXA_ETARIA"] = pd.cut(df["PA_IDADE"], bins=faixas, labels=nomes, right=False)

    return df
