WITH tb_join AS (

    SELECT 
        t1.dtRef,
        t1.idCliente,
        t1.descLifeCycle,
        t2.descLifeCycle,
        CASE WHEN t2.descLifeCycle = '02-FIEL' THEN 1 ELSE 0 END AS flFiel

    FROM life_cycle AS t1

    LEFT JOIN life_cycle AS t2
    ON t1.idCliente = t2.idCliente
    AND date(t1.dtRef, '+28 day') = date(t2.dtRef)

    WHERE t1.dtRef <= '2025-08-01'
    AND substr(t1.dtRef,9,2) = '01'
)

SELECT * FROM tb_join
ORDER BY idCliente, dtRef
LIMIT 100