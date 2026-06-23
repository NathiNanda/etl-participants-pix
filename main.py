import logging
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logging.info("=== Iniciando o Pipeline de ETL do PIX ===")
    
    try:
        # Extract
        logging.info("Iniciando a etapa de Extração (Extract)...")
        caminho_bruto = extract_data()
        
        # Transform
        logging.info("Iniciando a etapa de Transformação (Transform)...")
        df_limpo = transform_data()
        
        # Load
        logging.info("Iniciando a etapa de Carga (Load)...")
        load_data(df_limpo)
        
        logging.info("=== Pipeline de ETL finalizado com SUCESSO! ===")
        
    except Exception as e:
        logging.error(f"Erro catastrófico durante a execução do ETL: {e}")
        raise e

if __name__ == "__main__":
    main()
