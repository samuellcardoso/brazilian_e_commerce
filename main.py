from logging_config import logger
from read_raw import read_raw
from transform import criar_base, dim_tempo, dim_cliente, lookup_cliente, lookup_tempo, fato_vendas 
from validate import validate, save_processed
from load import load_data

def main():
    logger.info('Iniciando Pipeline')
    
    clientes, pedidos, itens = read_raw()
    
    base = criar_base(pedidos, itens)
    
    dim_cliente_df = dim_cliente(clientes)
    base_com_cliente = lookup_cliente(base, dim_cliente_df)

    dim_tempo_df = dim_tempo(base)
    base_com_tempo = lookup_tempo(base_com_cliente, dim_tempo_df)
            
    fato_venda = fato_vendas(base_com_tempo)
        
    dados_validos = validate(fato_venda, dim_cliente_df, dim_tempo_df)
    if dados_validos:
        save_processed(fato_venda, dim_cliente_df, dim_tempo_df)
        
        dados_carregados = load_data(dim_cliente_df, dim_tempo_df, fato_venda)
        
        if dados_carregados:
            logger.info('Pipeline concluido com sucesso')
        else:
            logger.error('Falha no carregamento dos dados no PostgreSQL')
    else:
        logger.error('Dados invalidos')
        
if __name__ == '__main__':
    main()