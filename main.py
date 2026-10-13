from logging_config import logger
from read_raw import read_raw
from transform import criar_base, dim_cliente, dim_tempo, lookup_cliente, lookup_tempo, fato_vendas 
from validate import validate, save_processed
from load import load_data

def main():
    pass