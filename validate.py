import pandas as pd
import os
from logging_config import logger

def validate(f_venda, d_cliente, d_tempo):
    try:
        # cliente_id único na DIM_CLIENTE;
        if d_cliente['cliente_id'].duplicated().any():
            logger.error('Falha na validacao: cliente_id duplicado na dim_cliente')
            return False
        
        # tempo_id único na DIM_TEMPO;
        if d_tempo['tempo_id'].duplicated().any():
            logger.error('Falha na validacao: tempo_id duplicado na dim_tempo')
            return False
        
        # venda_id único na fato;
        if f_venda['venda_id'].duplicated().any():
            logger.error('Falha na validacao: venda_id duplicado na fato_venda')
            return False
        
        # nenhum cliente_id da fato sem correspondência;
        if f_venda['cliente_id'].isna().any():
            logger.error(f'Falha na validacao: cliente_id com {f_venda["cliente_id"].isna().sum()} nulos.')
            return False
        
        # nenhum tempo_id da fato sem correspondência;
        if f_venda['tempo_id'].isna().any():
            logger.error(f'Falha na validacao: tempo_id com {f_venda["tempo_id"].isna().sum()} nulos.')
            return False
        
        # nenhuma venda_id da fato sem correspondência;
        if f_venda['venda_id'].isna().any():
            logger.error(f'Falha na validacao: venda_id com {f_venda["venda_id"].isna().sum()} nulos.')
            return False
        
        # cliente_id da fato tem que estar na dim_cliente
        clientes_invalidos = ~f_venda['cliente_id'].isin(d_cliente['cliente_id'])
        if clientes_invalidos.any():
            logger.error(f'Falha na validacao: {clientes_invalidos.sum()} cliente_id da fato nao existem na dim_cliente')
            return False
        
        # tempo_id da fato tem que estar na dim_tempo
        tempo_invalido = ~f_venda['tempo_id'].isin(d_tempo['tempo_id'])
        if tempo_invalido.any():
            logger.error(f'Falha na validacao: {tempo_invalido.sum()} tempo_id da fato nao existem na dim_tempo')
            return False
        
        if f_venda[['price', 'freight_value']].isna().any().any():
            logger.error('Falha na validacao: price ou freight_value tem valores nulos.')
            return False
        
        # venda_id tem que ser inteiro
        if not pd.api.types.is_integer_dtype(f_venda['venda_id']):
            logger.error('Falha na validacao: venda_id nao esta com tipo inteiro')
            return False
        
        # cliente_id tem que ser inteiro
        if not pd.api.types.is_integer_dtype(f_venda['cliente_id']):
            logger.error('Falha na validacao: cliente_id nao esta com tipo inteiro')
            return False
        
        # tempo_id tem que ser inteiro
        if not pd.api.types.is_integer_dtype(f_venda['tempo_id']):
            logger.error('Falha na validacao: tempo_id nao esta com tipo inteiro')
            return False
        
        # price tem que ser float
        if not pd.api.types.is_float_dtype(f_venda['price']):
            logger.error('Falha na validacao: price nao esta com tipo float')
            return False
        
        # freight_value tem que ser float
        if not pd.api.types.is_float_dtype(f_venda['freight_value']):
            logger.error('Falha na validacao: freight_value nao esta com tipo float')
            return False

        logger.info('Dados validados com sucesso.')
        
        return True
    
    except Exception:
        logger.exception('Erro na validacao dos dados.')
        raise
    
def save_processed(fato_venda, dim_cliente, dim_tempo):  
    try:
        os.makedirs('./data_lake/processed/', exist_ok=True)

        fato_venda.to_csv('./data_lake/processed/fato_venda.csv', index=False, encoding='utf-8')
        dim_cliente.to_csv('./data_lake/processed/dim_cliente.csv', index=False, encoding='utf-8')
        dim_tempo.to_csv('./data_lake/processed/dim_tempo.csv', index=False, encoding='utf-8')
        
        logger.info('Arquivos salvos na camada data_lake/processed.')
    except Exception:
        logger.exception('Erro no salvamento dos arquivos processed.')
        raise