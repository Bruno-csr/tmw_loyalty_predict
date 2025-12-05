-- Monthly Active Users

WITH tb_daily As (

    SELECT DISTINCT
            date(substr(DtCriacao, 0, 11)) AS DtDia,
            IdCliente
            
    FROM transacoes
    ORDER BY dtDia
),

tb_distinct_day as (
SELECT 
    DISTINCT DtDia AS dtRef
FROM tb_daily
)

SELECT 
    t1.dtRef,
    count(DISTINCT IdCliente) as MAU,
    count(DISTINCT t2.DtDia) as DiasAtras

FROM tb_distinct_day AS t1

LEFT JOIN tb_daily AS t2
ON t2.DtDia <= t1.dtRef
AND julianday(t1.dtRef) - julianday(t2.DtDia) < 28

GROUP BY t1.dtRef

ORDER BY t1.dtRef ASC
