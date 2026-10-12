#%%
import pandas as pd
from extract import df_cliente_original, df_pedidos_original, df_item_pedidos_original
from logging_config import logger

merged = df_pedidos_original.merge(df_item_pedidos_original, on='order_id')

df_antigo = merged[['order_id', 'order_item_id', 'customer_id', 'order_purchase_timestamp', 'price', 'freight_value']]

def dim_tempo():
    try:
        df = df_antigo[['order_purchase_timestamp']].copy()
        
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

        df['tempo_id'] = df['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
        df['data'] = df['order_purchase_timestamp'].dt.date
        df['ano'] = df['order_purchase_timestamp'].dt.year
        df['mes'] = df['order_purchase_timestamp'].dt.month
        df['dia'] = df['order_purchase_timestamp'].dt.day
        df['dia_semana'] = df['order_purchase_timestamp'].dt.day_name()

        df_tempo = df[['tempo_id', 'data', 'ano', 'mes', 'dia', 'dia_semana']].drop_duplicates(subset='tempo_id')
        
        logger.info(f'dim_tempo criada com sucesso | registros={len(df_tempo)}')
        
        return df_tempo
    
    except Exception:
        logger.exception('Erro na criacao da dim_tempo.')
        raise
    
def dim_cliente():
    try:
        df = df_cliente_original[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']].drop_duplicates().copy()
        df['cliente_id'] = range(1, len(df) + 1)
        
        df_cliente = df[['cliente_id', 'customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']]
        
        logger.info(f'dim_cliente criada com sucesso | registros={len(df_cliente)}')
        
        return df_cliente 
    
    except Exception:
        logger.exception('Erro na criacao da dim_cliente.')
        raise
    
def lookup_cliente(dim_cliente_df):
    try:
        base = df_antigo.merge(dim_cliente_df[['cliente_id', 'customer_id']], on='customer_id')
        base_com_cliente = base[['order_id', 'order_item_id', 'cliente_id', 'customer_id', 'order_purchase_timestamp', 'price', 'freight_value']]
        
        logger.info(f'lookup cliente concluido | antes={len(df_antigo)} | depois={len(base_com_cliente)}')
        
        return base_com_cliente
    
    except Exception:
        logger.exception('Erro no lookup cliente.')
        raise
    
def lookup_tempo(base_com_cliente, dim_tempo_df):
    try:
        base = base_com_cliente.copy()
        
        base['order_purchase_timestamp'] = pd.to_datetime(base['order_purchase_timestamp'])
        base['data'] = base['order_purchase_timestamp'].dt.date
        base_com_tempo = base.merge(dim_tempo_df[['tempo_id', 'data']], on='data')
        
        logger.info(f'lookup tempo concluido | antes={len(df_antigo)} | depois={len(base_com_tempo)}')
        
        return base_com_tempo
    
    except Exception:
        logger.exception('Erro no lookup tempo.')
        raise

def fato_vendas(fato):
    try:
        df = fato.copy()
        
        df['venda_id'] = range(1, len(df) + 1)
        fato_venda = df[['venda_id', 'order_id', 'order_item_id', 'cliente_id', 'tempo_id', 'price', 'freight_value']]
        
        logger.info(f'fato_vendas criada com sucesso | registros={len(fato_venda)}')
        
        return fato_venda
    
    except Exception:
        logger.exception('Erro na criacao da fato_vendas.')
        raise
    
        
dim_cliente_df = dim_cliente()
dim_tempo_df = dim_tempo()
base_com_cliente = lookup_cliente(dim_cliente_df)
base_com_tempo = lookup_tempo(base_com_cliente, dim_tempo_df)

fato = base_com_tempo[
    [
        'order_id',
        'order_item_id',
        'cliente_id',
        'tempo_id',
        'customer_id',
        'order_purchase_timestamp',
        'data',
        'price',
        'freight_value'
    ]
]

fato_venda = fato_vendas(fato)