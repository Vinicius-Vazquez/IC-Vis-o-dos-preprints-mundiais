import sqlite3
from src.config import DB_PATH

def get_db_connection():
    """Cria e retorna uma conexão SQLite configurada com o modo WAL para concorrência e performance."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ativa Write-Ahead Logging e otimizações de I/O
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    """Inicializa as tabelas do banco de dados para preprints e autores."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela principal de preprints
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preprints (
            id TEXT PRIMARY KEY,
            doi TEXT,
            title TEXT,
            publication_date TEXT,
            year INTEGER,
            type TEXT,
            cnpq_area TEXT,
            has_orcid INTEGER
        );
    """)
    
    # Tabela de autores associados (normalizada para análises de coautoria)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_id TEXT,
            author_id TEXT,
            name TEXT,
            orcid TEXT,
            institution TEXT,
            FOREIGN KEY (work_id) REFERENCES preprints(id) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    conn.close()