import pandas as pd
from logging_config import logger

def criar_base(pedidos: pd.DataFrame, itens: pd.DataFrame) -> pd.DataFrame:
    try:
        base = pedidos.merge(itens, on='order_id')
        
        base = base[['order_id', 'order_item_id', 'customer_id', 'order_purchase_timestamp', 'price', 'freight_value']].copy()
        
        logger.info(f'Base consolidada criada | registros={len(base)}')
        
        return base
    
    except Exception:
        logger.exception('Erro na criacao da base consolidada')
        raise
    

def dim_tempo(base: pd.DataFrame) -> pd.DataFrame:
    try:
        df_tempo = base[['order_purchase_timestamp']].copy()
        
        df_tempo['order_purchase_timestamp'] = pd.to_datetime(df_tempo['order_purchase_timestamp'])

        df_tempo['tempo_id'] = df_tempo['order_purchase_timestamp'].dt.strftime('%Y%m%d').astype(int)
        df_tempo['data'] = df_tempo['order_purchase_timestamp'].dt.date
        df_tempo['ano'] = df_tempo['order_purchase_timestamp'].dt.year
        df_tempo['mes'] = df_tempo['order_purchase_timestamp'].dt.month
        df_tempo['dia'] = df_tempo['order_purchase_timestamp'].dt.day
        df_tempo['dia_semana'] = df_tempo['order_purchase_timestamp'].dt.day_name()

        df_tempo = df_tempo[['tempo_id', 'data', 'ano', 'mes', 'dia', 'dia_semana']].drop_duplicates(subset='tempo_id')
        
        logger.info(f'dim_tempo criada com sucesso | registros={len(df_tempo)}')
        
        return df_tempo
    
    except Exception:
        logger.exception('Erro na criacao da dim_tempo.')
        raise
    
def dim_cliente(clientes: pd.DataFrame) -> pd.DataFrame:
    try:
        df_cliente = clientes[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']].drop_duplicates().copy()
        
        df_cliente['cliente_id'] = range(1, len(df_cliente) + 1)
        
        df_cliente = df_cliente[['cliente_id', 'customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']]
        
        logger.info(f'dim_cliente criada com sucesso | registros={len(df_cliente)}')
        
        return df_cliente 
    
    except Exception:
        logger.exception('Erro na criacao da dim_cliente.')
        raise
    
def lookup_cliente(base: pd.DataFrame, dim_cliente_df: pd.DataFrame) -> pd.DataFrame:
    try:
        base_com_cliente = base.merge(dim_cliente_df[['cliente_id', 'customer_id']], on='customer_id')
        
        base_com_cliente = base_com_cliente[['order_id', 'order_item_id', 'cliente_id', 'customer_id', 'order_purchase_timestamp', 'price', 'freight_value']]

        logger.info(f'lookup cliente concluido | antes={len(base)} | depois={len(base_com_cliente)}')
        
        return base_com_cliente
    
    except Exception:
        logger.exception('Erro no lookup cliente.')
        raise
    
def lookup_tempo(base_com_cliente: pd.DataFrame, dim_tempo_df: pd.DataFrame) -> pd.DataFrame:
    try:
        base = base_com_cliente.copy()
        
        base['order_purchase_timestamp'] = pd.to_datetime(base['order_purchase_timestamp'])
        base['data'] = base['order_purchase_timestamp'].dt.date
        
        base_com_tempo = base.merge(dim_tempo_df[['tempo_id', 'data']], on='data')
        
        base_com_tempo = base_com_tempo[['order_id', 'order_item_id', 'cliente_id', 'tempo_id', 'customer_id', 'order_purchase_timestamp', 'data', 'price', 'freight_value']]
        
        logger.info(f'lookup tempo concluido | antes={len(base)} | depois={len(base_com_tempo)}')
        
        return base_com_tempo
    
    except Exception:
        logger.exception('Erro no lookup tempo.')
        raise

def fato_vendas(base_com_tempo: pd.DataFrame) -> pd.DataFrame:
    try:
        fato_venda = base_com_tempo.copy()
        
        fato_venda['venda_id'] = range(1, len(fato_venda) + 1)
        
        fato_venda = fato_venda[['venda_id', 'order_id', 'order_item_id', 'cliente_id', 'tempo_id', 'price', 'freight_value']]
        
        logger.info(f'fato_vendas criada com sucesso | registros={len(fato_venda)}')
        
        return fato_venda
    
    except Exception:
        logger.exception('Erro na criacao da fato_vendas.')
        raise