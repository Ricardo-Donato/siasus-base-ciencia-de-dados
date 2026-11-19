# SIASUS — Análise para Gestão Municipal de Saúde

Projeto acadêmico da disciplina Programação para Ciência de Dados. A análise
explora a produção ambulatorial do SIASUS e apresenta indicadores para apoiar a
gestão municipal de saúde de Ijuí/RS.

## Organização

- `scripts_gerais/script_completo_dbsia.sql`: cria o banco `dbsia`, suas tabelas
  e carrega tabelas auxiliares.
- `scripts_gerais/carregar_dados_tabela_pars.sql`: exemplo de carga do PARS em
  lote com `LOAD DATA INFILE`. Ajuste o caminho ao computador e ao servidor
  MySQL usados pelo grupo.
- `scripts_gerais/04-gera-dimtempo-mysql.sql`: cria a dimensão mensal com
  atributos de mês, bimestre, trimestre e semestre.
- `scripts_gerais/view.sql`: cria a view `dbsia.pa_ijui`, com produção dos
  estabelecimentos localizados em Ijuí e dimensões descritivas.
- `T3 - Análise e Visualização SIASUS.ipynb`: notebook com as etapas de
  exploração, preparação, indicadores, tabelas e gráficos.
- `analises_geradas/csv/`: tabelas CSV produzidas pelas análises. A pasta pode
  conter saídas de execuções anteriores do notebook.
- `analises_geradas/img/`: gráficos PNG produzidos pelas análises. A pasta pode
  conter saídas de execuções anteriores do notebook.
- `arquivos_convertidos/`: tabelas auxiliares convertidas para CSV, DBF, DBC e
  SQL.

## Dados necessários

Os dados de produção PARS, necessários para gerar os indicadores, não estão
incluídos nesta cópia do repositório. Acesse a página oficial de
[Transferência de Arquivos do DATASUS](https://datasus.saude.gov.br/transferencia-de-arquivos/)
e filtre os arquivos da produção ambulatorial do SIASUS pela competência
**julho de 2026** e pela UF **RS**. O arquivo esperado pelo padrão de nomes é
`PARS2607`, dividido em `PARS2607a.dbc` e `PARS2607b.dbc`. Baixe as duas partes
para incluir todos os registros do período.

Os arquivos SIASUS também estão no diretório FTP
[`SIASUS/200801_/Dados/`](ftp://ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/).

Converta os dois DBCs para CSV. O exemplo em
[`carregar_dados_tabela_pars.sql`](scripts_gerais/carregar_dados_tabela_pars.sql)
espera um único `PARS2607.csv`; combine nele as linhas dos dois CSVs, mantendo
somente um cabeçalho. Como alternativa, ajuste o SQL para carregar cada CSV
separadamente, ignorando o cabeçalho de cada arquivo. Em ambos os casos, ajuste
o caminho local conforme a configuração do servidor MySQL.
Os CSVs em `arquivos_convertidos/csv/` são tabelas auxiliares de municípios,
não substituem o PARS.

## Preparação do MySQL

Use MySQL 8. Prepare o banco nesta ordem:

1. Revise `scripts_gerais/script_completo_dbsia.sql` e execute-o para criar o
   banco e carregar as tabelas auxiliares.
2. Carregue o CSV PARS na tabela `dbsia.pars`. Ajuste o caminho, delimitadores,
   codificação e versão do servidor conforme o arquivo recebido e a configuração
   local do MySQL.
3. Execute `scripts_gerais/04-gera-dimtempo-mysql.sql`.
4. Execute `scripts_gerais/view.sql` para criar `dbsia.pa_ijui`.

`script_completo_dbsia.sql` começa com `DROP DATABASE IF EXISTS dbsia` e recria
o banco. A execução apaga todo o conteúdo de `dbsia`; use-a em uma instalação
que possa ser recriada ou salve antes os dados que precisa preservar. A carga do
PARS exige que o servidor MySQL tenha acesso ao CSV e permissão para executar
`LOAD DATA INFILE`.

Depois da carga, confira a quantidade de registros em `dbsia.pars` com:

```sql
SELECT COUNT(*) AS total_registros FROM dbsia.pars;
```

## Executar as análises no notebook

Depois de preparar o MySQL, abra `T3 - Análise e Visualização SIASUS.ipynb` na
raiz do repositório pelo Jupyter ou VS Code. Execute as células de cima para
baixo. O notebook solicita usuário e senha do MySQL, carrega `dbsia.pa_ijui` uma
vez e salva tabelas CSV em
`analises_geradas/csv/` e gráficos PNG em `analises_geradas/img/`. A leitura
pode demorar e requer memória suficiente para manter a view em um DataFrame.

Instale as dependências no mesmo ambiente/kernel selecionado para o notebook:

```bash
python -m pip install jupyter pandas mysql-connector-python matplotlib seaborn
```

O notebook depende da tabela `DIMTEMPO` e da view `dbsia.pa_ijui`, criada com a
versão atual de `scripts_gerais/view.sql`. A view precisa incluir `PA_PROC_ID`
e `PA_TPUPS`. A preparação converte `pa_idade` em faixas etárias e preserva
`pa_flidade` como indicador de compatibilidade da idade com o procedimento.

O notebook é o fluxo de análise mantido no repositório. Ele carrega a view uma
vez e gera as tabelas e os gráficos consolidados.

O ranking por estabelecimento depende do preenchimento correto da junção com a
tabela CNES. Se `Estabelecimento` estiver ausente, o notebook registra essa
limitação e não apresenta um ranking como se fosse confiável. Com somente um
mês, os resumos mensal, bimestral e trimestral descrevem o período disponível;
não permitem avaliar tendências ou picos históricos.

## Fontes e período

Os dados vêm dos arquivos de produção ambulatorial do SIASUS/DATASUS e das
tabelas auxiliares de estabelecimentos, procedimentos, CBO, CID e municípios
presentes no repositório. A análise usa o mês de movimento
**julho de 2026 (2026-07)** e a view filtrada para estabelecimentos localizados em Ijuí
(`pa_ufmun = '431020'`). O CSV PARS usado não está versionado neste repositório;
o arquivo e o nome exato devem ser obtidos pelo método detalhado no notebook.

O nosso grupo combinou com o professor analisar somente um mês devido ao volume dos
dados. Por isso, não são apresentadas tendências históricas; os resumos de mês,
bimestre e trimestre referem-se ao único mês disponível.
