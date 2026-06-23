# Pipeline ETL & Dashboard de Participantes do PIX 📊

Este projeto é um pipeline de Engenharia de Dados ponta a ponta (End-to-End) que extrai dados da API pública de participantes do PIX da **BrasilAPI**, limpa e transforma esses dados utilizando **Python** e **Pandas**, carrega-os em um banco de dados relacional **SQLite** local e exibe análises interativas através de um dashboard construído com **Streamlit** e **Altair**.

O objetivo deste projeto é demonstrar a estruturação de um pipeline de dados profissional, utilizando modularização de código, boas práticas de Data Lake, bancos de dados relacionais locais e criação de interfaces de dados eficientes e leves.

---

## 🛠️ Arquitetura do Pipeline

O pipeline de dados segue a estrutura modular clássica de engenharia de software:

```mermaid
graph TD
    API["BrasilAPI (JSON)"] -- Requests --> Extract["Extract (extract.py)"]
    Extract -- Salva Bruto --> Raw["Landing Zone (data/raw/)"]
    Raw -- Pandas (read_json) --> Transform["Transform (transform.py)"]
    Transform -- Limpeza & Enriquecimento --> CleanDF["DataFrame Limpo"]
    CleanDF -- SQLite Connection --> Load["Load (load.py)"]
    Load -- Tabela participantes_pix --> DB[("Banco de Dados (pix.db)")]
    DB -- Query com Cache --> Streamlit["Dashboard (dashboard.py)"]
