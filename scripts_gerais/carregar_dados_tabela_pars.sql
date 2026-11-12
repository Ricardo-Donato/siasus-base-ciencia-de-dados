-- Substituir pelo nome correto do arquivo .csv 
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/PARS2608.csv' INTO TABLE pars CHARACTER SET latin1 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS;
-- Ele precisa estar dentro de 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'
