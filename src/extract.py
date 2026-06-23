import requests
import logging
import os
from datetime import datetime
import json

def extract_data():
    """
    It extracts PIX participant data from BrasilAPI and 
    saves the raw file in JSON format to the data/raw folder.
    """
    # Making the request
    url = "https://brasilapi.com.br/api/pix/v1/participants"

    print(f"Iniciando extração da API {url}")
    resposta = requests.get(url)

    logging.info(f"Status Code: {resposta.status_code}")
    print(f"Status Code: {resposta.status_code}")
    
    # Simple validation
    if resposta.status_code != 200:
        logging.error("Status Code diferente de 200")
        raise Exception(f"Falha da extração. Status Code: {resposta.status_code}")


    # This ensures traceability and allows for data reprocessing if business rules change
    # Creating folder if doesn't exist
    folder_raw = "data/raw"
    os.makedirs(folder_raw, exist_ok=True)

    # Creating a unique name based on the date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_arquivo = os.path.join(folder_raw, f"pix_raw_{timestamp}.json")

    # Converting response to json and saving it
    arquivo_json = resposta.json()
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        # dump() take the variable and put it into the file
        # indent=4 this helps the file look nice and readable if you open it in Notepad
        json.dump(arquivo_json, arquivo, indent=4, ensure_ascii=False)

    print(f"Dados extraidos com sucesso! Arquivo: {caminho_arquivo}")
    return caminho_arquivo

# The block below is for testing this file directly
if __name__ == "__main__":
    # Configure basic logging for testing
    logging.basicConfig(level=logging.INFO)
    extract_data()