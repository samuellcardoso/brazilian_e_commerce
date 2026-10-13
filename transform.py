import pandas as pd
from logging_config import logger

def criar_base(pedidos: pd.DataFrame, itens: pd.DataFrame) -> pd.DataFrame:
    try:
        merged = pedidos.merge(itens, on='order_id')
        
        base = merged[['order_id', 'order_item_id', 'customer_id', 'order_purchase_timestamp', 'price', 'freight_value']].copy()
        
        logger.info(f'Base consolidada criada | registros={len(base)}')
        
        return base
    
    except Exception:
        logger.exception('Erro na criacao da base consolidada')
        raise
    

def dim_tempo(base: pd.DataFrame) -> pd.DataFrame:
    try:
        df = base[['order_purchase_timestamp']].copy()
        
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
    
def dim_cliente(clientes: pd.DataFrame) -> pd.DataFrame:
    try:
        df = clientes[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']].drop_duplicates().copy()
        
        df['cliente_id'] = range(1, len(df) + 1)
        
        df_cliente = df[['cliente_id', 'customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']]
        
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
        base_cliente = base_com_cliente.copy()
        
        base_cliente['order_purchase_timestamp'] = pd.to_datetime(base_cliente['order_purchase_timestamp'])
        base_cliente['data'] = base_cliente['order_purchase_timestamp'].dt.date
        base = base_cliente.merge(dim_tempo_df[['tempo_id', 'data']], on='data')
        
        base_com_tempo = base[['order_id', 'order_item_id', 'cliente_id', 'tempo_id', 'customer_id', 'order_purchase_timestamp', 'data', 'price', 'freight_value']]
        
        logger.info(f'lookup tempo concluido | antes={len(base_cliente)} | depois={len(base_com_tempo)}')
        
        return base_com_tempo
    
    except Exception:
        logger.exception('Erro no lookup tempo.')
        raise

def fato_vendas(base_com_tempo: pd.DataFrame) -> pd.DataFrame:
    try:
        df = base_com_tempo.copy()
        
        df['venda_id'] = range(1, len(df) + 1)
        fato_venda = df[['venda_id', 'order_id', 'order_item_id', 'cliente_id', 'tempo_id', 'price', 'freight_value']]
        
        logger.info(f'fato_vendas criada com sucesso | registros={len(fato_venda)}')
        
        return fato_venda
    
    except Exception:
        logger.exception('Erro na criacao da fato_vendas.')
        raise