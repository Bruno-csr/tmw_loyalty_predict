WITH tb_life_cycle_atual AS (
    SELECT 
        IdCliente,
        descLifeCycle
    FROM life_cycle
    WHERE dtRef = date('2025-09-01', '-1 day')
)

SELECT 
    IdCliente,
    descLifeCycle
FROM life_cycle
WHERE dtRef = date('2025-09-01', '-29 day')
