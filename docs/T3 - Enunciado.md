T3 - Análise de Dados do SIASUS para Apoio à Gestão Municipal de Saúde 
Situação-problema: 
A Secretaria Municipal de Saúde de Ijuí/RS enfrenta o desafio de planejar, monitorar e avaliar os serviços ambulatoriais prestados à população do município e aos pacientes provenientes de outros municípios e regiões. 
Para apoiar essas atividades, dispõe dos dados do Sistema de Informações Ambulatoriais do SUS (SIASUS), disponibilizados pelo DATASUS. Esses dados contêm informações sobre procedimentos ambulatoriais, estabelecimentos de saúde, diagnósticos, características dos pacientes e valores relacionados à produção ambulatorial, conforme a modalidade de registro. 
Entretanto, o grande volume e a complexidade dos dados dificultam sua utilização para identificar padrões, avaliar os serviços prestados e produzir informações que subsidiem a tomada de decisão. Além disso, possíveis valores ausentes, inconsistências e duplicidades podem comprometer a confiabilidade das análises. 
Diante desse cenário, a Secretaria Municipal de Saúde contratou uma equipe de Ciência de Dados para desenvolver uma solução capaz de armazenar, processar, analisar e visualizar os dados históricos do SIASUS, transformando os registros disponíveis em informações relevantes para a gestão municipal. 
Pergunta norteadora: 
Como transformar os dados do SIASUS em informações que permitam compreender a produção ambulatorial, identificar diferenças e possíveis problemas nos serviços de saúde e subsidiar o planejamento e a tomada de decisão da Secretaria Municipal de Saúde de Ijuí? 
Objetivo: 
Desenvolver uma solução de análise de dados capaz de produzir indicadores, análises e representações gráficas que auxiliem o planejamento, o monitoramento e a avaliação dos serviços ambulatoriais de Ijuí e da região. 
O trabalho será desenvolvido em três etapas interdependentes, distribuídas em três aulas práticas. 
Aula 1 - Construção e preparação do banco de dados 
Desafio: Como organizar milhões de registros do SIASUS em um banco de dados relacional que permita realizar consultas e análises de maneira confiável?
Nesta etapa, os grupos deverão obter, preparar e importar os dados do SIASUS para o MySQL, garantindo que o banco de dados esteja operacional para as próximas etapas. O modelo conceitual a seguir apresenta de forma formal e simplificada o banco de dados. 

Passo a passo para criar o banco de dados: 
1. Obtenção dos dados: acessar o repositório do DATASUS e obter os arquivos do SIASUS, no formato .dbc, referentes aos períodos definidos para a atividade, incluindo os arquivos de produção ambulatorial (PARS) e as tabelas auxiliares necessárias. 
2. Conversão dos arquivos: converter os arquivos .dbc para .dbf, utilizando o TABWIN (disponível no site do DATASUS). 
3. Estruturação do banco: examinar os atributos disponíveis, identificar os tipos de dados e preparar os scripts SQL de criação das tabelas. Nessa etapa também utiliza-se o TABWIN. 
4. Criação e carga: criar o banco de dados no MySQL e importar os registros. Para arquivos menores, poderão ser utilizados scripts de inserção. Para arquivos de grande volume, como o PARS, deverá ser realizada a conversão para CSV e a importação em lote por meio da instrução LOAD DATA INFILE. 
5. Validação: verificar a estrutura das tabelas, a quantidade de registros importados e possíveis erros de conversão ou importação. 
6. Consultas SQL: executar consultas que demonstrem o funcionamento do banco e a recuperação correta dos registros. 
Exemplo de Instrução para fazer a importação de grandes volumes de dados:
Os grupos poderão utilizar a instrução LOAD DATA INFILE, conforme a documentação do MySQL: 
Referência: https://dev.mysql.com/doc/refman/8.4/en/load-data.html 
Execute a instrução utilizando o cliente MySQL na linha de comando (como administrador), observando as permissões e configurações do servidor, para evitar dificuldades de importação pelo MySQL Workbench. 
Exemplo: 
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 
8.0/Uploads/PARS2608.csv' INTO TABLE pars CHARACTER SET latin1 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS; 
Entrega da Aula 1: 
O grupo deverá demonstrar ao professor: 
● Banco de dados criado e carregado. 
● Estrutura das tabelas e quantidade de registros importados. 
● Scripts SQL utilizados. 
● Execução de consultas que comprovem o funcionamento do ambiente.
Aula 2 - Análise exploratória e processamento de dados com Pandas 
1. Análise Exploratória de Dados 
● Verificar o número de linhas e colunas do banco de dados. 
● Conferir tipos de variáveis (numéricas, categóricas, textuais). 
● Calcular estatísticas descritivas iniciais (média, mediana, mínimo, máximo, distribuição de frequências). 
● Identificar valores ausentes (por exemplo, NaN, campos vazios) e valores inválidos (por exemplo, idade fora da faixa, sexo diferente de M/F, CIDs não existentes). 
2. Limpeza e Preparação dos Dados 
Aplicar estratégias para melhorar a qualidade dos dados: 
● Valores nulos: apagar as linhas? preencher com "Não informado"? ● Duplicações: remover registros duplicados. 
3. Análises Estratégicas para o Gestor de Saúde do Município 
1. Volume e Perfil dos Procedimentos 
● Quantos procedimentos ambulatoriais foram realizados em Ijuí no último mês, bimestre e trimestre (crie a tabela de granularidade temporal a partir do arquivo 04-gera-dimtempo-mysql.sql). 
● Distribuição por especialidade/procedimento (consultas básicas, exames de imagem, oncologia, psiquiatria, etc). 
● Evolução temporal: picos e quedas na demanda. 
2. Produção por Estabelecimento de Saúde 
● Ranking de produção dos estabelecimentos (HCI, Hospital Bom Pastor, UBS, clínicas conveniadas). 
● Comparar volume de procedimentos aprovados x produzidos. 
3. Perfil Demográfico e Epidemiológico da População Atendida 
● Distribuição por sexo e faixa etária. 
● Principais diagnósticos (CID) atendidos (hipertensão, diabetes, câncer, etc). 4. Fluxos Regionais e Acesso 
● Municípios de origem dos pacientes atendidos em Ijuí. 
● Quantos atendimentos feitos em Ijuí são de moradores de outros municípios. 5. Recursos Financeiros 
● Total de valores aprovados pelo SUS para Ijuí x valores produzidos. ● Diferença entre produzidos e aprovados. 
● Evolução do gasto médio por procedimento ambulatorial. 
6. Foco em Áreas Críticas 
● Oncologia: quimioterapia e radioterapia (aprovados x produzidos). ● Saúde mental: atendimentos psiquiátricos e psicológicos. 
● Atenção básica: consultas e procedimentos nas UBS, acompanhamento de doenças crônicas. 
Entrega da Aula 2: 
O grupo deverá apresentar: 
● Código Python executável com acesso ao banco MySQL.
●DataFrameseprocedimentosdeexploraçãoepreparação.
Aula 3 - Visualização de dados e interpretação dos resultados 
Desafio: Como apresentar os resultados das análises de forma clara e objetiva para que a Secretaria Municipal de Saúde possa identificar situações relevantes e tomar decisões fundamentadas? 
Nesta etapa, os grupos deverão utilizar bibliotecas de visualização em Python para transformar os resultados obtidos com Pandas em gráficos e representações que facilitem a interpretação das informações. 
Atividades 
1. Seleção dos indicadores: identificar os resultados mais relevantes das análises realizadas na aula anterior. 
2. Construção das visualizações: desenvolver gráficos utilizando Matplotlib, Seaborn, Plotly ou outras bibliotecas de visualização em Python. 
3. Adequação das representações: selecionar os tipos de gráficos conforme as características dos dados e os objetivos das análises. 
4. Comparação dos resultados: representar visualmente diferenças entre períodos, estabelecimentos, procedimentos, municípios e indicadores financeiros. 5. Interpretação: explicar os principais resultados, identificando padrões, diferenças e situações que merecem atenção da gestão municipal. 
Entrega da Aula 3 
O grupo deverá apresentar: 
● Código Python utilizado para gerar as visualizações. 
● Gráficos relacionados às questões analisadas. 
● Interpretação dos resultados. 
Aula 4 – Apresentação e avaliação dos resultados 
Desafio: Como demonstrar que a solução desenvolvida transforma os dados do SIASUS em informações relevantes para a gestão municipal de saúde? 
Cada grupo deverá apresentar o trabalho desenvolvido, demonstrando a integração entre o banco de dados relacional, o processamento com Pandas e a visualização dos resultados. 
Organização da apresentação 
1. Construção do banco de dados 
Demonstrar a estrutura das tabelas, a carga dos registros e o funcionamento das consultas SQL.
2. Análise de dados com Pandas 
Apresentar os principais procedimentos de exploração, preparação e análise, incluindo os indicadores calculados. 
3. Visualização dos resultados 
Apresentar os gráficos desenvolvidos. 
Entrega final 
Cada grupo deverá entregar o link do repositório no GitHub, contendo os scripts SQL, o código Python utilizado nas análises e visualizações e um arquivo README.md com instruções de execução, identificação das fontes e períodos analisados. 
Apresentação dos resultados, com demonstração do ambiente, do código desenvolvido, dos gráficos e das conclusões. 
Critérios de avaliação – 60 pontos
Critério 
Pontuação
Criação, carga e validação do banco de dados 
10
Exploração, limpeza e preparação dos dados 
10
Implementação das análises com Python 
10
Desenvolvimento das questões de análise 
12
Visualização e interpretação dos resultados 
10
Apresentação e reprodutibilidade 
8
Total 
60



