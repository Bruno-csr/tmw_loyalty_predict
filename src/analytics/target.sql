WITH tb_join AS (

    SELECT 
        t1.dtRef,
        t1.idCliente,
        t1.descLifeCycle,
        t2.descLifeCycle,
        CASE WHEN t2.descLifeCycle = '02-FIEL' THEN 1 ELSE 0 END AS flFiel,
        --aleatoriadade dos dados
        ROW_NUMBER() OVER (PARTITION BY t1.idCliente ORDER BY random()) AS randomCol
 
    FROM life_cycle AS t1

    LEFT JOIN life_cycle AS t2
    ON t1.idCliente = t2.idCliente
    AND date(t1.dtRef, '+28 day') = date(t2.dtRef)

    WHERE ((t1.dtRef >= '2024-03-01' AND t1.dtRef <= '2025-08-01') 
            OR t1.dtRef = '2025-09-01')
    AND t1.descLifeCycle <> '05-ZUMBI'
),

tb_cohort AS (

    SELECT 
        t1.dtRef,
        t1.idCliente,
        t1.flFiel

    FROM tb_join AS t1
    WHERE randomCol <= 2
    ORDER BY idCliente, dtRef
)

SELECT t1.*
FROM tb_cohort AS t1

LEFT JOIN fs_transacional AS t2
ON t1.idCliente = t2.idCliente
AND t1.dtRef = t2.dtRef

LIMIT 100

--https://youtu.be/Co3BVGxTJfc