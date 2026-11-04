from src.ingestion.collector import PreprintCollector
from src.database.connection import get_db_connection, init_db
from src.config import DB_PATH

def test_collector_sample_run():
    """Testa se o coletor executa a amostra e insere registros no banco com sucesso."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    
    collector = PreprintCollector()
    collector.run_sample_collection(max_records=5) # Amostra leve de 5 registros
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM preprints;")
    total_preprints = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as total FROM authors;")
    total_authors = cursor.fetchone()["total"]
    
    conn.close()
    
    assert total_preprints > 0, "O coletor deveria ter persistido pelo menos um preprint."
    assert total_authors >= 0, "A tabela de autores deve estar acessível."