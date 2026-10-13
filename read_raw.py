import pandas as pd
from logging_config import logger

def read_raw():
    try:
        df_cliente_original = pd.read_csv('./data_lake/raw/olist_customers_dataset.csv')
        df_pedidos_original = pd.read_csv('./data_lake/raw/olist_orders_dataset.csv')
        df_item_pedidos_original = pd.read_csv('./data_lake/raw/olist_order_items_dataset.csv')
        
        logger.info(f'Arquivos raw carregados com sucesso. | clientes={len(df_cliente_original)} | pedidos={len(df_pedidos_original)} | itens={len(df_item_pedidos_original)}')
        
        return df_cliente_original, df_pedidos_original, df_item_pedidos_original
    except Exception:
        logger.exception('Erro na leitura dos arquivos raw.')
        raise