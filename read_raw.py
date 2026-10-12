import pandas as pd


df_cliente_original = pd.read_csv('./data_lake/raw/olist_customers_dataset.csv')
df_pedidos_original = pd.read_csv('./data_lake/raw/olist_orders_dataset.csv')
df_item_pedidos_original = pd.read_csv('./data_lake/raw/olist_order_items_dataset.csv')