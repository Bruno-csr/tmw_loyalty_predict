SELECT
    dtRef,
    descLifeCycle,
    count(*) AS qtdeCliente

FROM life_cycle

WHERE descLifeCycle <> '05-ZUMBI'
AND dtRef = (SELECT Max(dtRef) FROM life_cycle)

GROUP BY dtRef, descLifeCycle
ORDER BY dtRef, descLifeCycle