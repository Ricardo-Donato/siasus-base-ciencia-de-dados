# SIASUS — Análise para Gestão Municipal de Saúde

<p>Projeto acadêmico da disciplina Programação para Ciência de Dados.</p>
<p>A análise explora a produção ambulatorial do SIASUS e apresenta indicadores para apoiar a gestão municipal de saúde de Ijuí/RS.</p>

## Organização

- `scripts_gerais/script_completo_dbsia.sql`: cria o banco `dbsia`, suas tabelas e carrega tabelas auxiliares.
- `scripts_gerais/carregar_dados_tabela_pars.sql`: exemplo de carga do PARS em lote com `LOAD DATA INFILE`. É de suma importância ajustar o caminho presente no comando para que fique em conformidade ao seu computador e ao servidor MySQL.
- `scripts_gerais/04-gera-dimtempo-mysql.sql`: cria a dimensão mensal com atributos de mês, bimestre, trimestre e semestre.
- `scripts_gerais/view.sql`: cria a view `dbsia.pa_ijui`, com produção dos estabelecimentos localizados em Ijuí e dimensões descritivas.
- `T3 - Análise e Visualização SIASUS.ipynb`: notebook com as etapas de exploração, preparação, indicadores, tabelas e gráficos.
- `analises_geradas/`:  A pasta contém saídas de execuções anteriores do notebook.
- `analises_geradas/csv/`: tabelas CSV produzidas pelas análises.
- `analises_geradas/img/`: gráficos PNG produzidos pelas análises.
- `arquivos_convertidos/`: tabelas auxiliares convertidas para CSV, DBF, DBC e  SQL.

## Dados necessários

Os dados de produção PARS, necessários para gerar os indicadores, não estão incluídos nesta cópia do repositório. Acesse a página oficial de [Transferência de Arquivos do DATASUS](https://datasus.saude.gov.br/transferencia-de-arquivos/) e filtre os arquivos da produção ambulatorial do SIASUS pela competência **julho de 2026** e pela UF **RS** (veja o anexo abaixo). O arquivo esperado pelo padrão de nomes é `PARS2607a`.

<img width="936" height="728" alt="image" src="https://github.com/user-attachments/assets/31dbee47-0413-4996-9988-32d9fa4107ac" />

Os arquivos SIASUS também estão no diretório FTP `ftp://ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/`. Procure por `PARS2607a` nesse diretório e copie para o seu computador.

Em seguida, converta o arquivo DBC para DBF. Para fazer essa conversão, é necessário obter o `TABWIN415.zip` disponível no diretório FTP `ftp://ftp.datasus.gov.br/tabwin/tabwin/`.
<img width="944" height="435" alt="image" src="https://github.com/user-attachments/assets/bc45719e-5631-4cfb-93ca-c84a54c9b454" />

Copie para o seu computador, descompacte, acesse essa pasta e arraste o arquivo DBC sobre o app dbf2dbc.exe. Com ele convertido para DBF, use a interface do `TabWin415.exe` para ver o DBF e converta para o csv no botão localizado no canto superior esquerdo da aplicação.

<img width="102" height="93" alt="image" src="https://github.com/user-attachments/assets/d13aaf72-499d-484b-99fc-457638e32fdc" />


O exemplo em [`carregar_dados_tabela_pars.sql`](scripts_gerais/carregar_dados_tabela_pars.sql) espera um único `PARS2607.csv`. Não se esqueça de ajustar o caminho local conforme a configuração do servidor MySQL. Os CSVs em `arquivos_convertidos/csv/` são tabelas auxiliares de municípios, não substituem o PARS.

## Preparação do MySQL

Prepare o banco nesta ordem:

1. Revise `scripts_gerais/script_completo_dbsia.sql` e execute-o para criar o banco e carregar as tabelas auxiliares.
2. Carregue o CSV PARS na tabela `dbsia.pars`. Ajuste o caminho, delimitadores, codificação e versão do servidor conforme o arquivo recebido e a configuração local do MySQL.
3. Execute `scripts_gerais/04-gera-dimtempo-mysql.sql`.
4. Execute `scripts_gerais/view.sql` para criar `dbsia.pa_ijui`.

`script_completo_dbsia.sql` começa com `DROP DATABASE IF EXISTS dbsia` e recria o banco. A execução apaga todo o conteúdo de `dbsia`; use-a em uma instalação que possa ser recriada ou salve antes os dados que precisa preservar. A carga do PARS exige que o servidor MySQL tenha acesso ao CSV e permissão para executar `LOAD DATA INFILE`. Recomenda-se fortemente executar esse último comando no Command Line do MySQL, pois há a possibilidade de ocorrer timeout no Workbench.

Depois da carga, confira a quantidade de registros em `dbsia.pars` com:

```sql
SELECT COUNT(*) AS total_registros FROM dbsia.pars;
```

## Executar as análises no notebook

Depois de preparar o MySQL, abra `T3 - Análise e Visualização SIASUS.ipynb` na raiz do repositório pelo Jupyter ou VS Code. Execute as células de cima para baixo. O notebook solicita usuário e senha do MySQL, carrega `dbsia.pa_ijui` uma vez e salva tabelas CSV em `analises_geradas/csv/` e gráficos PNG em `analises_geradas/img/`. A leitura pode demorar e requer memória suficiente para manter a view em um DataFrame.

Instale as dependências no mesmo ambiente/kernel selecionado para o notebook:

```bash
python -m pip install jupyter pandas mysql-connector-python matplotlib seaborn
```

O notebook depende da tabela `DIMTEMPO` e da view `dbsia.pa_ijui`, criada com a versão atual de `scripts_gerais/view.sql`. A view precisa incluir `PA_PROC_ID` e `PA_TPUPS`. A preparação converte `pa_idade` em faixas etárias e preserva `pa_flidade` como indicador de compatibilidade da idade com o procedimento.

O notebook é o fluxo de análise mantido no repositório. Ele carrega a view uma vez e gera as tabelas e os gráficos consolidados.

O ranking por estabelecimento depende do preenchimento correto da junção com a tabela CNES. Se `Estabelecimento` estiver ausente, o notebook registra essa limitação e não apresenta um ranking como se fosse confiável. Com somente um mês, os resumos mensal, bimestral e trimestral descrevem o período disponível; não permitem avaliar tendências ou picos históricos.

## Fontes e período

Os dados vêm dos arquivos de produção ambulatorial do SIASUS/DATASUS e das tabelas auxiliares de estabelecimentos, procedimentos, CBO, CID e municípios presentes no repositório. A análise usa o mês de movimento **julho de 2026 (2026-07)** e a view filtrada para estabelecimentos localizados em Ijuí (`pa_ufmun = '431020'`). O CSV PARS usado não está versionado neste repositório; o arquivo e o nome exato devem ser obtidos pelo método detalhado no notebook.

O nosso grupo combinou com o professor analisar somente um mês devido ao volume dos dados. Por isso, não são apresentadas tendências históricas; os resumos de mês, bimestre e trimestre referem-se ao único mês disponível.
