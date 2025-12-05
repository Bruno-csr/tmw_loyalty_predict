WITH tb_life_cycle_atual AS (
    SELECT 
        IdCliente,
        qtdeFrequencia,
        descLifeCycle AS descLifeCycleAtual

    FROM life_cycle
    WHERE dtRef = date('2025-10-01', '-1 day')
),

tb_life_cycle_D28 AS (
    SELECT 
        IdCliente,
        descLifeCycle AS descLifeCycleD28
    FROM life_cycle
    WHERE dtRef = date('2025-10-01', '-29 day')
),

tb_share_ciclos AS (
    SELECT 
        IdCliente,
        1. * SUM(CASE WHEN descLifeCycle = '01-CURIOSO' THEN 1 ELSE 0 END) / COUNT (*) AS pctCurioso,
        1. * SUM(CASE WHEN descLifeCycle = '02-FIEL' THEN 1 ELSE 0 END) / COUNT (*) AS pctFiel,
        1. * SUM(CASE WHEN descLifeCycle = '02-RECONQUISTADA' THEN 1 ELSE 0 END) / COUNT (*) AS pctReconquistada,
        1. * SUM(CASE WHEN descLifeCycle = '02-REBORN' THEN 1 ELSE 0 END) / COUNT (*) AS pctReborn,
        1. * SUM(CASE WHEN descLifeCycle = '03-TURISTA' THEN 1 ELSE 0 END) / COUNT (*) AS pctTurista,
        1. * SUM(CASE WHEN descLifeCycle = '04-DESENCANTADA' THEN 1 ELSE 0 END) / COUNT (*) AS pctDesencantada,
        1. * SUM(CASE WHEN descLifeCycle = '05-ZUMBI' THEN 1 ELSE 0 END) / COUNT (*) AS pctZumbi

    FROM life_cycle
    WHERE dtRef < '2025-10-01'

    ORDER BY IdCliente
),

tb_avg_ciclo AS (
    SELECT 
        descLifeCycleAtual,
        avg(qtdeFrequencia) AS avgFrequnciaGrupo

    FROM tb_life_cycle_atual
    GROUP BY descLifeCycleAtual
),

tb_join AS (
    SELECT 
        t1.*,
        t2.descLifeCycleD28 AS descLifeCycle_D28,
        t3.pctCurioso,
        t3.pctFiel,
        t3.pctReconquistada,
        t3.pctReborn,
        t3.pctTurista,
        t3.pctDesencantada,
        t3.pctZumbi,
        t4.avgFrequnciaGrupo,
        1. * t1.qtdeFrequencia / t4.avgFrequnciaGrupo AS ratioFrquenciaGrupo

    FROM tb_life_cycle_atual AS t1

    LEFT JOIN tb_life_cycle_D28 AS t2
    ON t1.IdCliente = t2.IdCliente

    LEFT JOIN tb_share_ciclos AS t3
    ON t1.IdCliente = t3.IdCliente

    LEFT JOIN tb_avg_ciclo AS t4
    ON t1.descLifeCycleAtual = t4.descLifeCycleAtual
)

SELECT 
    date('2025-10-01', '-1 day') AS dtRef,
    *
FROM tb_join