import os
from pathlib import Path

# Caminhos base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CHECKPOINT_DIR = DATA_DIR / "checkpoints"

# Garante a existência dos diretórios de dados
for d in [RAW_DIR, PROCESSED_DIR, CHECKPOINT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Banco de dados SQLite otimizado para alta volumetria
DB_PATH = DATA_DIR / "preprints.db"

# Parâmetros da API OpenAlex (Polite Pool com e-mail institucional)
OPENALEX_EMAIL = "vazquez@aluno.cefetmg.br"
OPENALEX_BASE_URL = "https://api.openalex.org/works"