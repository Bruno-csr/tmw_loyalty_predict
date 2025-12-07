WITH tb_trasnsacao AS (
    SELECT 
        *,
        substr(DtCriacao, 0 ,11) AS dtDia,
        CAST(substr(DtCriacao, 12, 2) AS int) AS dtHora

    FROM transacoes
    WHERE dtCriacao < '2025-10-01'
),
-- Frequência em Dias (D7, D14, D28, D56, Vida)
-- Frequência em Transações (D7, D14, D28, D56, Vida)
-- Valor de pontos (pos, neg, saldo) - D7, D14, D28, D56, Vida
-- Quantidade de transações por dia (D7, D14, D28, D56)
tb_agg_trasnsacao AS (

    SELECT 

        IdCliente,

        max(julianday('2025-10-01', '-1 day') - julianday(DtCriacao)) AS idadeDias,

        count(DISTINCT dtDia) AS qtdeAtivacaoVida,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-7 day') THEN dtDia END) AS qtdeAtivacaoD7,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-14 day') THEN dtDia END) AS qtdeAtivacaoD14,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-28 day') THEN dtDia END) AS qtdeAtivacaoD28,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-56 day') THEN dtDia END) AS qtdeAtivacaoD56,

        count(DISTINCT IdTransacao) AS qtdeTransacaoVida,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-7 day') THEN IdTransacao END) AS qtdeTransacaoD7,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-14 day') THEN IdTransacao END) AS qtdeTransacaoD14,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-28 day') THEN IdTransacao END) AS qtdeTransacaoD28,
        count(DISTINCT CASE WHEN dtDia >= date('2025-10-01', '-56 day') THEN IdTransacao END) AS qtdeTransacaoD56,

        sum(qtdePontos) AS saldoVida,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-7 day') THEN qtdePontos ELSE 0 END) AS saldoD7,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-14 day') THEN qtdePontos ELSE 0 END) AS saldoD14,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-28 day') THEN qtdePontos ELSE 0 END) AS saldoD28,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-56 day') THEN qtdePontos ELSE 0 END) AS saldoD56,

        sum(CASE WHEN qtdePontos > 0 THEN qtdePontos ELSE 0 END) AS qtdePontosPosVida,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-7 day') AND qtdePontos > 0 THEN qtdePontos ELSE 0 END) AS qtdePontosPosD7,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-14 day') AND qtdePontos > 0 THEN qtdePontos ELSE 0 END) AS qtdePontosPosD14,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-28 day') AND qtdePontos > 0 THEN qtdePontos ELSE 0 END) AS qtdePontosPosD28,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-56 day') AND qtdePontos > 0 THEN qtdePontos ELSE 0 END) AS qtdePontosPosD56,

        sum(CASE WHEN qtdePontos < 0 THEN qtdePontos ELSE 0 END) AS qtdePontosNegVida,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-7 day') AND qtdePontos < 0 THEN qtdePontos ELSE 0 END) AS qtdePontosNegD7,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-14 day') AND qtdePontos < 0 THEN qtdePontos ELSE 0 END) AS qtdePontosNegD14,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-28 day') AND qtdePontos < 0 THEN qtdePontos ELSE 0 END) AS qtdePontosNegD28,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-56 day') AND qtdePontos < 0 THEN qtdePontos ELSE 0 END) AS qtdePontosNegD56,

        -- dados de horas em UTC, logo, devemos adicionar 3 horas (BRASIL está em UTC-3)
        count(CASE WHEN dtHora BETWEEN 7+3 AND 11+3 THEN IdTransacao END) AS qtdeTransacaoManha,
        count(CASE WHEN dtHora BETWEEN 12+3 AND 18+3 THEN IdTransacao END) AS qtdeTransacaoTarde,
        count(CASE WHEN dtHora > 18+3 OR dtHora < 7+3 THEN IdTransacao END) AS qtdeTransacaoNoite,

        1. * count(CASE WHEN dtHora BETWEEN 7+3 AND 11+3 THEN IdTransacao END) / count(IdTransacao) AS pctTransacaoManha,
        1. * count(CASE WHEN dtHora BETWEEN 12+3 AND 18+3 THEN IdTransacao END) / count(IdTransacao) AS pctTransacaoTarde,
        1. * count(CASE WHEN dtHora > 18+3 OR dtHora < 7+3 THEN IdTransacao END) / count(IdTransacao) AS pctTransacaoNoite

    FROM tb_trasnsacao
    GROUP BY IdCliente

),

-- Percentual de ativação no MAU
tb_agg_calc AS (

    SELECT 
        *,
        COALESCE(1. * qtdeTransacaoVida / qtdeAtivacaoVida, 0) AS QtdeTransacaoDiaVida,
        COALESCE(1. * qtdeTransacaoD7 / qtdeAtivacaoD7, 0) AS QtdeTransacaoDiaD7,
        COALESCE(1. * qtdeTransacaoD14 / qtdeAtivacaoD14, 0) AS QtdeTransacaoDiaD14,
        COALESCE(1. * qtdeTransacaoD28 / qtdeAtivacaoD28, 0) AS QtdeTransacaoDiaD28,
        COALESCE(1. * qtdeTransacaoD56 / qtdeAtivacaoD56, 0) AS QtdeTransacaoDiaD56,

        COALESCE(1. * qtdeTransacaoD28 / 28, 0) AS pctAtivacaoMAU

    FROM tb_agg_trasnsacao
),

-- Qtde Horas por dia por cliente
tb_horas_dia AS (
    SELECT 
        IdCliente,
        dtDia,
        (max(julianday(dtCriacao)) - min(julianday(dtCriacao))) * 24 as duracao

    FROM tb_trasnsacao
    GROUP BY idCliente, dtDia
),

-- Qtde Horas totais por cliente
tb_horas_cliente AS (
    SELECT
        idCliente,
        sum(duracao) AS qtdeHorasVida,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-7 day') THEN duracao ELSE 0 END) AS qtdeHorasD7,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-14 day') THEN duracao ELSE 0 END) AS qtdeHorasD14,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-28 day') THEN duracao ELSE 0 END) AS qtdeHorasD28,
        sum(CASE WHEN dtDia >= date('2025-10-01', '-56 day') THEN duracao ELSE 0 END) AS qtdeHorasD56

    FROM tb_horas_dia
    GROUP BY idCliente
),

-- Diferença de dias entre as ativações
tb_lag_dia AS (
    SELECT 
        IdCliente,
        dtDia,
        LAG(dtDia) OVER (PARTITION BY IdCliente ORDER BY dtDia) AS lagDia
    FROM tb_horas_dia
),

-- Média da diferença de dias entre as ativações
tb_intervalo_dias AS (
    SELECT 
        IdCliente,
        avg(julianday(dtDia) - julianday(lagDia)) AS avgIntntervaloDiasVida,
        avg(CASE WHEN dtDia >= date('2025-10-01', '-28 day') THEN julianday(dtDia) - julianday(lagDia) END) AS avgIntntervaloDiasD28
    FROM tb_lag_dia
    GROUP BY IdCliente
),

tb_share_produtos AS (
    SELECT
        idCliente,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Airflow Lover' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeAirflowLover,
        1. * COUNT(CASE WHEN DescNomeProduto = 'ChatMessage' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeChatMessage,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Resgatar Ponei' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeResgatarPonei,
        1. * COUNT(CASE WHEN DescNomeProduto = 'R Lover' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeRLover,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Presença Streak' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdePresencaStreak,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Lista de presença' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeListadepresenca,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Reembolso: Troca de Pontos StreamElements' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeReembolsoStreamElements,
        1. * COUNT(CASE WHEN DescNomeProduto = 'Troca de Pontos StreamElement' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeTrocaStreamElement,
        1. * COUNT(CASE WHEN DescCategoriaProduto = 'rpg' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeRPG,
        1. * COUNT(CASE WHEN DescCategoriaProduto = 'churn_model' THEN t1.IdTransacao END) / COUNT(t1.IdTransacao) AS qtdeChurnModel
    FROM tb_trasnsacao AS t1

    LEFT JOIN transacao_produto AS t2
    ON t1.IdTransacao = t2.IdTransacao

    LEFT JOIN produtos AS t3
    ON t2.IdProduto = t3.IdProduto

    GROUP BY IdCliente
),

tb_join AS (

    SELECT 
        t1.*,
        t2.qtdeHorasVida,
        t2.qtdeHorasD7,
        t2.qtdeHorasD14,
        t2.qtdeHorasD28,
        t2.qtdeHorasD56,
        t3.avgIntntervaloDiasVida,
        t3.avgIntntervaloDiasD28,
        t4.qtdeAirflowLover,
        t4.qtdeChatMessage,
        t4.qtdeResgatarPonei,
        t4.qtdeRLover,
        t4.qtdePresencaStreak,
        t4.qtdeListadepresenca,
        t4.qtdeReembolsoStreamElements,
        t4.qtdeTrocaStreamElement,
        t4.qtdeRPG,
        t4.qtdeChurnModel  
        
    FROM tb_agg_calc AS t1

    LEFT JOIN tb_horas_cliente AS t2
    ON t1.IdCliente = t2.IdCliente

    LEFT JOIN tb_intervalo_dias AS t3
    ON t3.IdCliente = t1.IdCliente

    LEFT JOIN tb_share_produtos AS t4
    ON t1.IdCliente = t4.IdCliente
)

SELECT 
    date('2025-10-01', '-1 day') AS dtRef,
    *
FROM tb_join