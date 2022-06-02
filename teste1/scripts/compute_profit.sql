WITH transacoes_realizadas AS (
    select "contratos"."cliente_id",
        "contratos"."nome",
        "contratos"."contrato_id",
        CASE
            WHEN "contratos"."percentual" IS NULL THEN 0
            ELSE "contratos"."percentual" / 100
        END AS percentual,
        "transacao"."valor_total",
        CASE
            WHEN "transacao"."percentual_desconto" IS NULL THEN 0
            ELSE "transacao"."percentual_desconto" / 100
        END AS percentual_desconto
    from (
            select "cliente"."cliente_id",
                "cliente"."nome",
                "contrato"."contrato_id",
                "contrato"."percentual"
            from "desafio_engenheiro"."dbo"."cliente" cliente
                inner join "desafio_engenheiro"."dbo"."contrato" contrato on cliente.cliente_id = contrato.cliente_id
            where "contrato"."ativo" = 1
        ) contratos
        inner join "desafio_engenheiro"."dbo"."transacao" transacao on "contratos"."contrato_id" = "transacao"."contrato_id"
)
SELECT nome,
    ROUND(SUM((valor_liquido * percentual)), 2) as lucro_por_cliente
from (
        SELECT nome,
            (valor_total * (1 - percentual_desconto)) as valor_liquido,
            percentual
        from transacoes_realizadas
    ) valor_liquido_transacoes
group by valor_liquido_transacoes.nome