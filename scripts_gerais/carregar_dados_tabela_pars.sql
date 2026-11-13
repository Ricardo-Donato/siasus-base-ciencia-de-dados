-- Substituir pelo nome correto do arquivo .csv 
-- Esse foi o caso de exemplo utilizado para fazer a importação de grandes volumes de dados
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/PARS2607.csv' INTO TABLE pars CHARACTER SET latin1 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
-- Ele precisa estar dentro de 'C:/ProgramData/MySQL/MySQL Server x.x/Uploads'
