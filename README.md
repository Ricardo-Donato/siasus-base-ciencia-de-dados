# SIASUS — Análise para Gestão Municipal de Saúde

Projeto acadêmico da disciplina Programação para Ciência de Dados. O objetivo é
explorar a produção ambulatorial do SIASUS e produzir indicadores que apoiem a
gestão municipal de saúde de Ijuí/RS.

## Organização

- `scripts_gerais/script_completo_dbsia.sql`: cria o banco `dbsia`, suas tabelas
  e carrega tabelas auxiliares.
- `scripts_gerais/carregar_dados_tabela_pars.sql`: exemplo de carga do PARS em
  lote com `LOAD DATA INFILE`; o caminho precisa ser ajustado ao computador e ao
  servidor MySQL usados pelo grupo.
- `scripts_gerais/04-gera-dimtempo-mysql.sql`: cria a dimensão mensal com
  atributos de mês, bimestre, trimestre e semestre.
- `scripts_gerais/view.sql`: cria a view `dbsia.pa_ijui`, com produção dos
  estabelecimentos localizados em Ijuí e dimensões descritivas.
- `py/analise_exploratoria.py`: exploração inicial e resumos por período,
  estabelecimento, procedimento, sexo, diagnóstico e município de origem.
- `py/conexao.py`: conexão local com MySQL usada pelos scripts Python.
- `arquivos_convertidos/`: tabelas auxiliares convertidas para CSV, DBF, DBC e
  SQL.

## Dados necessários

Os dados de produção PARS são necessários para gerar os indicadores. Os arquivos
PARS não estão incluídos nesta cópia do repositório; o exemplo de carga usa um
CSV chamado `PARS2607.csv`, que deve ser substituído pelo arquivo e período
fornecidos ao grupo. Os CSVs em `arquivos_convertidos/csv/` são tabelas
auxiliares de municípios, não substituem o PARS.

## Preparação do MySQL

Use MySQL 8 para os scripts fornecidos. A ordem geral de preparação é:

1. Revise `scripts_gerais/script_completo_dbsia.sql` e execute-o para criar o
   banco e carregar as tabelas auxiliares.
2. Carregue o CSV PARS na tabela `dbsia.pars`. Ajuste o caminho, delimitadores,
   codificação e versão do servidor conforme o arquivo recebido e a configuração
   local do MySQL.
3. Execute `scripts_gerais/04-gera-dimtempo-mysql.sql`.
4. Execute `scripts_gerais/view.sql` para criar `dbsia.pa_ijui`.

**Atenção:** `script_completo_dbsia.sql` começa com `DROP DATABASE IF EXISTS
dbsia`; executá-lo apaga e recria esse banco. Faça isso apenas em uma instalação
que possa ser recriada ou depois de salvar o que precisa preservar. A carga PARS
depende do CSV estar acessível ao servidor MySQL e das permissões de `LOAD DATA
INFILE`.

## Executar a exploração em Python

Instale as dependências em um ambiente Python:

```bash
python -m pip install pandas mysql-connector-python
```

Depois, na pasta `py/`, execute:

```bash
python analise_exploratoria.py
```

O script pede o usuário e a senha do MySQL local e consulta `dbsia.pa_ijui`.
Ele imprime os resumos no terminal e não altera registros no banco. A idade é
mantida como código nesta exploração; sua conversão em faixa etária deve
considerar também `pa_flidade`.

## Fontes e período

Fonte dos dados: Sistema de Informações Ambulatoriais do SUS (SIASUS/DATASUS) e
tabelas auxiliares distribuídas com o projeto. Registre aqui, antes da entrega,
os arquivos PARS utilizados e os meses/anos abrangidos pela análise.
