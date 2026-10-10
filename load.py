from db_connection import conn
from validate import fato_venda, dim_cliente_df, dim_tempo_df

def criar_tabelas():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS dim_cliente (
                        cliente_id INT PRIMARY KEY,
                        customer_id VARCHAR(100) UNIQUE NOT NULL,
                        customer_unique_id VARCHAR(100),
                        customer_zip_code_prefix INT,
                        customer_city VARCHAR(100),
                        customer_state CHAR(2)
                    )'''
            )
            
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS dim_tempo (
                        tempo_id INT PRIMARY KEY,
                        data DATE NOT NULL,
                        ano INT,
                        mes INT,
                        dia INT,
                        dia_semana VARCHAR(15)
                    )'''
            )
            
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS fato_venda (
                        venda_id INT PRIMARY KEY,
                        order_id VARCHAR(100) NOT NULL,
                        order_item_id INT,
                        cliente_id INT NOT NULL,
                        tempo_id INT NOT NULL,
                        price NUMERIC(10, 2),
                        freight_value NUMERIC(10, 2),
                        
                        FOREIGN KEY (cliente_id) REFERENCES dim_cliente(cliente_id),
                        FOREIGN KEY (tempo_id) REFERENCES dim_tempo(tempo_id)
                    )'''
            )  
    except Exception as e:
        print(f'Erro ao criar as tabelas: {e}')
        conn.rollback()
        return False
    else:
        print('Tabelas criadas com sucesso.')
        conn.commit()
        return True

def inserir_dim_cliente():
    try:
        with conn.cursor() as cursor:
            for _, row in dim_cliente_df.iterrows():
                cursor.execute('''
                    INSERT INTO dim_cliente (
                        cliente_id,
                        customer_id,
                        customer_unique_id,
                        customer_zip_code_prefix,
                        customer_city,
                        customer_state
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT(cliente_id)
                    DO UPDATE SET
                        customer_id = EXCLUDED.customer_id,
                        customer_unique_id = EXCLUDED.customer_unique_id,
                        customer_zip_code_prefix = EXCLUDED.customer_zip_code_prefix,
                        customer_city = EXCLUDED.customer_city,
                        customer_state = EXCLUDED.customer_state
                        ''', 
                        (
                            row['cliente_id'],
                            row['customer_id'],
                            row['customer_unique_id'],
                            row['customer_zip_code_prefix'],
                            row['customer_city'],
                            row['customer_state']
                        )
                )
    except Exception as e:
        conn.rollback()
        print(f'Erro ao inserir os dados na tabela dim_cliente: {e}')
        return False
    else:
        print('dim_cliente carregada com sucesso.')
        conn.commit()
        return True
    
def inserir_dim_tempo():
    try:
        with conn.cursor() as cursor:
            for _, row in dim_tempo_df.iterrows():
                cursor.execute('''
                    INSERT INTO dim_tempo (
                        tempo_id,
                        data,
                        ano,
                        mes,
                        dia,
                        dia_semana
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (tempo_id)
                    DO UPDATE SET
                        data = EXCLUDED.data,
                        ano = EXCLUDED.ano,
                        mes = EXCLUDED.mes,
                        dia = EXCLUDED.dia,
                        dia_semana = EXCLUDED.dia_semana
                               ''',
                        (
                            row['tempo_id'],
                            row['data'],
                            row['ano'],
                            row['mes'],
                            row['dia'],
                            row['dia_semana']
                        )
                )
    except Exception as e:
        conn.rollback()
        print(f'Erro ao inserir dados na tabela dim_tempo: {e}')
        return False
    else:
        conn.commit()
        print('dim_tempo carregada com sucesso.')
        return True
    
def inserir_fato_venda():
    try:
        with conn.cursor() as cursor:
            for _, row in fato_venda.iterrows():
                cursor.execute('''
                    INSERT INTO fato_venda (
                        venda_id,
                        order_id,
                        order_item_id,
                        cliente_id,
                        tempo_id,
                        price,
                        freight_value
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (venda_id)
                    DO UPDATE SET
                        order_id = EXCLUDED.order_id,
                        order_item_id = EXCLUDED.order_item_id,
                        cliente_id = EXCLUDED.cliente_id,
                        tempo_id = EXCLUDED.tempo_id,
                        price = EXCLUDED.price,
                        freight_value = EXCLUDED.freight_value
                               ''',
                        (
                            row['venda_id'],
                            row['order_id'],
                            row['order_item_id'],
                            row['cliente_id'],
                            row['tempo_id'],
                            row['price'],
                            row['freight_value']
                        )
                )
    except Exception as e:
        conn.rollback()
        print(f'Erro ao inserir os dados na tabela fato_vendas: {e}')
        return False
    else:
        conn.commit()
        print('fato_vendas carregada com sucesso')
        return True

tabelas = criar_tabelas()
if tabelas:
    clientes_ok = inserir_dim_cliente()
    
    if clientes_ok:
        tempo_ok = inserir_dim_tempo()
        
        if tempo_ok:
            inserir_fato_venda()