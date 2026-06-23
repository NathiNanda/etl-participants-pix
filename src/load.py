import os
import sqlite3

def load_data(df):
    """
    Receives a clean DataFrame and saves it to a table in the SQLite database.
    Ensures that the connection is closed correctly after writing.
    """
    # Save the dataframe to the SQLite database.
    folder_processed = "data/processed"
    os.makedirs(folder_processed, exist_ok=True)

    caminho_banco = os.path.join(folder_processed, "pix.db")
    print("Iniciando carga. Conectando ao banco de dados: ", caminho_banco)

    conexao = sqlite3.connect(caminho_banco)
    print("Conexão estabelecida com sucesso.")

    try:
        # Writes the data from the dataframe to the SQLite database.
        df.to_sql('participantes_pix', conexao, if_exists='replace', index=False)
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        raise e
    finally:
        # Close the connection.
        conexao.close()
        print("Carga concluída. Conexão encerrada.")

# Bloco para testar o arquivo diretamente
if __name__ == "__main__":
    # Apenas para testar se funciona, vamos importar o transform_data para gerar um DataFrame de teste
    from src.transform import transform_data
    
    # 1. Roda a transformação para pegar os dados
    df_teste = transform_data()
    
    # 2. Tenta carregar no banco
    load_data(df_teste)