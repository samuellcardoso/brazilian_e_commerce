-- Faturamento Total
SELECT 
  ROUND(SUM(price), 2) AS faturamento_total
FROM fato_venda;

-- Faturamento por mes
SELECT 
  t2.ano, 
  t2.mes, 
  ROUND(SUM(t1.price), 2) AS faturamento_mensal
FROM fato_venda AS t1
LEFT JOIN dim_tempo AS t2
  ON t1.tempo_id = t2.tempo_id
GROUP BY t2.ano, t2.mes
ORDER BY t2.ano, t2.mes;

-- Faturamento por estado
SELECT 
  t2.customer_state, 
  SUM(t1.price) AS faturamento_por_estado
FROM fato_venda AS t1
LEFT JOIN dim_cliente AS t2
  ON t1.cliente_id = t2.cliente_id
GROUP BY t2.customer_state
ORDER BY faturamento_por_estado DESC;

-- Faturamento por cidade
SELECT 
  t2.customer_state, 
  t2.customer_city, 
  ROUND(SUM(t1.price), 2) AS faturamento_por_cidade
FROM fato_venda AS t1
LEFT JOIN dim_cliente AS t2
  ON t1.cliente_id = t2.cliente_id
GROUP BY t2.customer_state, t2.customer_city 
ORDER BY faturamento_por_cidade DESC;

-- Frete medio por item
SELECT 
  ROUND(AVG(freight_value), 2) AS frete_medio
FROM fato_venda;

-- Ticket medio por pedido
WITH tb_total AS (
  SELECT 
    order_id, SUM(price) AS faturamento_por_pedido
  FROM fato_venda
  GROUP BY order_id
)
  
SELECT 
  ROUND(AVG(faturamento_por_pedido), 2) AS ticket_medio_por_pedido
FROM tb_total;

-- Quantidade de itens por cliente
SELECT 
  t2.cliente_id, 
  t2.customer_id, COUNT(*) AS qtd_itens
FROM fato_venda AS t1
LEFT JOIN dim_cliente AS t2
  ON t1.cliente_id = t2.cliente_id
GROUP BY t2.cliente_id, t2.customer_id
ORDER BY qtd_itens DESC;

-- Quantidade de pedidos por estado
SELECT 
  t2.customer_state, 
  COUNT(DISTINCT t1.order_id) AS qtd_pedidos
FROM fato_venda AS t1
LEFT JOIN dim_cliente AS t2
  ON t1.cliente_id = t2.cliente_id
GROUP BY t2.customer_state;

-- Media de itens por pedido
WITH itens_por_pedido AS (
  SELECT 
    order_id, 
    COUNT(*) AS qtd_itens
  FROM fato_venda
  GROUP BY order_id
)

SELECT 
  ROUND(AVG(qtd_itens), 2) AS media_itens_por_pedido
FROM itens_por_pedido;

-- Top 5 clientes que mais gastaram
SELECT 
  t2.cliente_id, 
  t2.customer_id, 
  ROUND(SUM(t1.price), 2) AS gasto_cliente
FROM fato_venda AS t1
LEFT JOIN dim_cliente AS t2
  ON t1.cliente_id = t2.cliente_id
GROUP BY t2.cliente_id, t2.customer_id
ORDER BY gasto_cliente DESC
LIMIT 5;