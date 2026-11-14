"""Exploração inicial e indicadores da produção ambulatorial de Ijuí.

Pré-requisitos:
    - MySQL com o banco ``dbsia`` carregado;
    - tabela ``DIMTEMPO`` e view ``dbsia.pa_ijui`` criadas;
    - dependências instaladas (ver ``requirements.txt`` do projeto, se houver).

O script consulta a view criada em ``scripts_gerais/view.sql`` e imprime
resumos exploratórios e tabelas agregadas. Ele não altera os dados no MySQL.
"""

from __future__ import annotations

import pandas as pd

import conexao


COLUNAS_NUMERICAS = [
    "pa_qtdpro",
    "pa_qtdapr",
    "pa_valpro",
    "pa_valapr",
]

COLUNAS_INDICADORES = [
    "pa_qtdpro",
    "pa_qtdapr",
    "pa_valpro",
    "pa_valapr",
]


def carregar_dados(connection) -> pd.DataFrame:
    """Carrega os registros da view de produção dos estabelecimentos de Ijuí."""
    consulta = "SELECT * FROM dbsia.pa_ijui"
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        return pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)


def preparar_dados(tabela: pd.DataFrame) -> pd.DataFrame:
    """Converte medidas e monta uma data mensal quando possível.

    ``pa_idade`` fica como campo categórico nesta etapa: sua interpretação
    depende de ``pa_flidade``, que informa a unidade/código de idade do SIASUS.
    """
    tabela = tabela.copy()
    for coluna in COLUNAS_NUMERICAS:
        if coluna in tabela.columns:
            tabela[coluna] = pd.to_numeric(tabela[coluna], errors="coerce")

    if "pa_idade" in tabela.columns:
        tabela["pa_idade"] = tabela["pa_idade"].astype("string")
    if "pa_flidade" in tabela.columns:
        tabela["pa_flidade"] = tabela["pa_flidade"].astype("string")

    if {"Ano", "Mes"}.issubset(tabela.columns):
        ano = pd.to_numeric(tabela["Ano"], errors="coerce")
        mes = pd.to_numeric(tabela["Mes"], errors="coerce")
        tabela["Data"] = pd.to_datetime(
            {"year": ano, "month": mes, "day": 1}, errors="coerce"
        )
        tabela["AnoMes"] = tabela["Data"].dt.to_period("M").astype("string")
    return tabela


def imprimir_tabela(titulo: str, tabela: pd.DataFrame) -> None:
    print(f"\n{titulo}")
    if tabela.empty:
        print("(sem registros)")
    else:
        print(tabela.to_string(index=False))


def imprimir_periodos_recentes(tabela: pd.DataFrame) -> None:
    """Resume o mês, bimestre e trimestre que contêm o mês mais recente.

    Os intervalos seguem os períodos de calendário usados pela DIMTEMPO:
    bimestres Jan-Fev, Mar-Abr, ... e trimestres Jan-Mar, Abr-Jun, etc.
    Se a view tiver somente parte do período, o resumo cobre os meses presentes.
    """
    if "Data" not in tabela.columns or tabela["Data"].notna().sum() == 0:
        print("\nNão há ano/mês válidos para resumir períodos recentes.")
        return

    dados = tabela.loc[tabela["Data"].notna()].copy()
    ultimo_mes = dados["Data"].max().to_period("M")
    mes_numero = ultimo_mes.month
    inicio_bimestre = pd.Period(
        year=ultimo_mes.year, month=((mes_numero - 1) // 2) * 2 + 1, freq="M"
    )
    inicio_trimestre = pd.Period(
        year=ultimo_mes.year, month=((mes_numero - 1) // 3) * 3 + 1, freq="M"
    )

    medidas = [c for c in COLUNAS_INDICADORES if c in dados.columns]
    periodos = [
        ("Mês mais recente", ultimo_mes, ultimo_mes),
        ("Bimestre mais recente", inicio_bimestre, inicio_bimestre + 1),
        ("Trimestre mais recente", inicio_trimestre, inicio_trimestre + 2),
    ]

    linhas = []
    for nome, inicio, fim in periodos:
        selecionados = dados.loc[
            dados["Data"].dt.to_period("M").between(inicio, fim)
        ]
        linha = {
            "Período": nome,
            "Intervalo": f"{inicio} a {fim}",
            "MesesComDados": int(
                selecionados["Data"].dt.to_period("M").nunique()
            ),
            "Registros": len(selecionados),
        }
        for coluna in medidas:
            linha[coluna] = selecionados[coluna].sum(min_count=1)
        linhas.append(linha)

    imprimir_tabela(
        "=== Produção e valores nos períodos recentes ===",
        pd.DataFrame(linhas),
    )
    print(
        "Períodos ancorados no mês mais recente encontrado na view; "
        "meses sem registros não entram nos totais."
    )


def analisar(tabela: pd.DataFrame) -> None:
    """Exibe exploração, qualidade e principais agregações."""
    print("\n=== Dimensão e tipos ===")
    print(f"Registros: {len(tabela):,}")
    print(f"Colunas: {len(tabela.columns)}")
    print("\nTipos de dados:")
    print(tabela.dtypes.to_string())

    print("\n=== Valores ausentes ===")
    print(tabela.isna().sum().sort_values(ascending=False).to_string())

    duplicados = int(tabela.duplicated().sum())
    print(f"\nLinhas duplicadas exatas: {duplicados:,}")
    print("Duplicações são apenas contabilizadas; nenhum registro é removido.")

    colunas_presentes = [c for c in COLUNAS_NUMERICAS if c in tabela.columns]
    if colunas_presentes:
        print("\n=== Estatísticas descritivas ===")
        print(tabela[colunas_presentes].describe().to_string())

    indicadores_presentes = [
        c for c in COLUNAS_INDICADORES if c in tabela.columns
    ]
    if indicadores_presentes:
        totais = tabela[indicadores_presentes].sum(min_count=1)
        print("\n=== Totais gerais ===")
        print(totais.to_string())
        if {"pa_qtdpro", "pa_qtdapr"}.issubset(totais.index):
            print(
                "Diferença entre quantidade produzida e aprovada: "
                f"{totais['pa_qtdpro'] - totais['pa_qtdapr']:,.0f}"
            )
        if {"pa_valpro", "pa_valapr"}.issubset(totais.index):
            print(
                "Diferença entre valor produzido e aprovado: R$ "
                f"{totais['pa_valpro'] - totais['pa_valapr']:,.2f}"
            )

    if "AnoMes" in tabela.columns:
        mensal = (
            tabela.groupby("AnoMes", dropna=False)
            .agg(
                Registros=("AnoMes", "size"),
                **{
                    nome: (coluna, "sum")
                    for nome, coluna in [
                        ("QuantidadeProduzida", "pa_qtdpro"),
                        ("QuantidadeAprovada", "pa_qtdapr"),
                        ("ValorProduzido", "pa_valpro"),
                        ("ValorAprovado", "pa_valapr"),
                    ]
                    if coluna in tabela.columns
                },
            )
            .reset_index()
            .sort_values("AnoMes")
        )
        imprimir_tabela("=== Produção mensal ===", mensal)

    imprimir_periodos_recentes(tabela)

    agregacoes = [
        ("Estabelecimento", "=== Produção por estabelecimento (top 20) ==="),
        ("Procedimento", "=== Procedimentos por quantidade produzida (top 20) ==="),
        ("pa_sexo", "=== Perfil por sexo ==="),
        ("Diagnostico", "=== Diagnósticos principais (top 20) ==="),
        ("MunicipioPaciente", "=== Municípios de origem (top 20) ==="),
    ]
    for dimensao, titulo in agregacoes:
        if dimensao not in tabela.columns:
            continue
        medidas = [c for c in indicadores_presentes if c in tabela.columns]
        resumo = (
            tabela.groupby(dimensao, dropna=False)
            .agg(Registros=(dimensao, "size"), **{c: (c, "sum") for c in medidas})
            .sort_values("pa_qtdpro" if "pa_qtdpro" in medidas else "Registros", ascending=False)
            .head(20)
            .reset_index()
        )
        imprimir_tabela(titulo, resumo)

    if "MunicipioPaciente" in tabela.columns:
        fora = tabela["MunicipioPaciente"].fillna("").str.strip().str.upper().ne("IJUI")
        print(
            "\nRegistros com município de origem diferente de Ijuí (ou não identificado): "
            f"{int(fora.sum()):,} de {len(tabela):,}"
        )
        print(
            "Observação: a contagem acima considera registros, não pacientes únicos; "
            "a view não identifica pacientes individualmente."
        )


def main() -> None:
    tabela = conexao.usar_conexao(carregar_dados)
    if tabela is None:
        print("Não foi possível carregar a view. Confira a conexão e o banco dbsia.")
        return
    if tabela.empty:
        print("A view dbsia.pa_ijui não retornou registros.")
        return
    analisar(preparar_dados(tabela))


if __name__ == "__main__":
    main()
