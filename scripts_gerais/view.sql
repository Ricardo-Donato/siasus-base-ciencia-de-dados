use dbsia;

drop view if exists pa_ijui;

CREATE OR REPLACE VIEW pa_ijui AS
SELECT
    -- 1. DIMENSÃO TEMPORAL
    dt.ano AS Ano,
    dt.mes AS Mes,
    dt.anobi AS AnoBimestre,
    dt.anotri AS AnoTrimestre,

    -- 2. ESTABELECIMENTO DE SAÚDE    
    ca.fantasia AS Estabelecimento,    

    -- 3. PROCEDIMENTO AMBULATORIAL    
    pro.ip_dscr AS Procedimento,

    -- 4. OCUPAÇÃO PROFISSIONAL    
    cb.ds_cbo AS Ocupacao,

    -- 5. PERFIL DEMOGRÁFICO
    pa.pa_sexo,
    pa.pa_idade,
    pa.pa_flidade,

    -- 6. DIAGNÓSTICO PRINCIPAL
    pa.pa_cidpri,
    cid.cd_descr AS Diagnostico,

    -- 7. MUNICÍPIO DO ESTABELECIMENTO    
    mun_est.ds_nome AS MunicipioEstabelecimento,

    -- 8. MUNICÍPIO DO PACIENTE    
    mun_pac.ds_nome AS MunicipioPaciente,    

    -- 9. PRODUÇÃO AMBULATORIAL
    pa.pa_qtdpro,
    pa.pa_qtdapr,

    -- 10. VALORES FINANCEIROS
    pa.pa_valpro,
    pa.pa_valapr

FROM pars AS pa

-- Estabelecimento de saúde
LEFT JOIN cadgerrs AS ca
    ON pa.pa_coduni = ca.cnes

-- Procedimento ambulatorial
LEFT JOIN procedimentos AS pro
    ON pa.pa_proc_id = pro.ip_cod

-- Ocupação profissional
LEFT JOIN cbo AS cb
    ON pa.pa_cbocod = cb.cbo

-- Diagnóstico principal
LEFT JOIN cid
    ON pa.pa_cidpri = cid.cd_cod

-- Município do estabelecimento
LEFT JOIN tb_municip AS mun_est
    ON pa.pa_ufmun = mun_est.co_municip

-- Município do paciente
LEFT JOIN tb_municip AS mun_pac
    ON pa.pa_munpcn = mun_pac.co_municip

-- Dimensão temporal (mês de movimento)
LEFT JOIN DIMTEMPO AS dt
    ON pa.pa_mvm = dt.anomes

-- Produção realizada nos estabelecimentos de Ijuí
WHERE pa.pa_ufmun = '431020';


select count(*) from pa_ijui;

select * from pa_ijui LIMIT 5;
