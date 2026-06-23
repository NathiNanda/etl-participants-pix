import pandas as pd
import logging
import glob
import os
import numpy as np

# Creates a new institution category column based on the institution's name
MAPA_CATEGORIAS = {
    "Cooperativa": ["COOPERATIVA", "COOP", "CREDIT"],
    "Fintech / IP": ["IP S.A.", "INSTITUICAO DE PAGAMENTO", "PAGAMENTOS"],
    "Banco": ["BANCO", "BCO"]
    }

def classificar_instituicao(nome):
    # If the name is empty (NaN), play in Others
    if pd.isna(nome):
        return "Outros"

    nome_maiusculo = str(nome).upper()

    # Scan the dictionary looking for a match
    for categoria, termos in MAPA_CATEGORIAS.items():
        for termo in termos:
            if termo in nome_maiusculo:
                return categoria
    
    return "Outros"

def transform_data():
    """
    Reads the latest JSON from the data/raw folder, cleans the data,
    filters metadata, normalizes strings, applies categorization
    and returns a clean and structured DataFrame.
    """
    folder_raw = "data/raw"

    # Get the most recent JSON file
    arquivos_raw = glob.glob(os.path.join(folder_raw, "*.json"))

    if arquivos_raw:
        arquivos_raw.sort()
        arquivo_recente = arquivos_raw[-1]

        df = pd.read_json(arquivo_recente)
        linhas = len(df)
        print(f"Lendo o arquivo: {arquivo_recente}")
        print(f"Dados extraídos com sucesso: {linhas} registros encontrados.")
        logging.info(f"Dados extraídos com sucesso: {linhas} registros encontrados.")
    else:
        print("Nenhum arquivo encontrado")

    # Remove metadata/garbage rows from the API
    df = df[df["modalidade_participacao"] != "Modalidade de Participação no Pix"]
    df = df[df["tipo_participacao"] != "Tipo de Participação no SPI"]

    # Replace the empty space with "Not informed"
    df["tipo_participacao"] = df["tipo_participacao"].replace("",np.nan)
    df["tipo_participacao"] = df["tipo_participacao"].fillna("Não informado")

    # Normalize column names and institution text (no spaces at the ends and no double spaces in the middle)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.replace(r'\s+', ' ', regex=True)

    df["categoria_instituicao"] = df["nome"].apply(classificar_instituicao)

    # Required columns
    df = df[['ispb','nome','modalidade_participacao','tipo_participacao','categoria_instituicao']]

    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df_teste = transform_data()

    # Displays the initial lines and information needed to validate the test
    print("\nVisualização das primeiras linhas:")
    print(df_teste.head())
    print("\nInformações do DataFrame:")
    df_teste.info()