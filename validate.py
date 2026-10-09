import pandas as pd
from transform import fato_venda, dim_cliente_df, dim_tempo_df

def validate(f_venda, d_cliente, d_tempo):
    # cliente_id único na DIM_CLIENTE;
    if d_cliente['cliente_id'].duplicated().any():
        return False
    
    # tempo_id único na DIM_TEMPO;
    if d_tempo['tempo_id'].duplicated().any():
        return False
    
    # venda_id único na fato;
    if f_venda['venda_id'].duplicated().any():
        return False
    
    # nenhum cliente_id da fato sem correspondência;
    if f_venda['cliente_id'].isna().any():
        return False
    
    # nenhum tempo_id da fato sem correspondência;
    if f_venda['tempo_id'].isna().any():
        return False
    
    # verificar nulos e tipos.
    if f_venda['venda_id'].isna().any():
        return False
    
    # cliente_id da fato tem que estar na dim_cliente
    if (~f_venda['cliente_id'].isin(d_cliente['cliente_id'])).any():
        return False
    
    # tempo_id da fato tem que estar na dim_tempo
    if (~f_venda['tempo_id'].isin(d_tempo['tempo_id'])).any():
        return False
    
    if f_venda[['price', 'freight_value']].isna().any().any():
        return False
    
    # venda_id tem que ser inteiro
    if not pd.api.types.is_integer_dtype(f_venda['venda_id']):
        return False
    
    # cliente_id tem que ser inteiro
    if not pd.api.types.is_integer_dtype(f_venda['cliente_id']):
        return False
    
    # tempo_id tem que ser inteiro
    if not pd.api.types.is_integer_dtype(f_venda['tempo_id']):
        return False
    
    # price tem que ser float
    if not pd.api.types.is_float_dtype(f_venda['price']):
        return False
    
    # freight_value tem que ser float
    if not pd.api.types.is_float_dtype(f_venda['freight_value']):
        return False

    return True
print(validate(fato_venda, dim_cliente_df, dim_tempo_df))