import os
from src.database.connection import get_db_connection, init_db
from src.config import DB_PATH

def test_database_initialization():
    """Testa se o banco de dados e as tabelas essenciais são criados corretamente."""
    if DB_PATH.exists():
        DB_PATH.unlink()  # Remove base antiga de testes se existir
        
    init_db()
    assert DB_PATH.exists(), "O arquivo do banco de dados SQLite não foi criado."
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()
    
    assert "preprints" in tables, "A tabela 'preprints' não foi encontrada."
    assert "authors" in tables, "A tabela 'authors' não foi encontrada."