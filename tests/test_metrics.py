from src.processing.metrics import BibliometricAnalyzer
from src.database.connection import init_db
from src.config import DB_PATH

def test_bibliometric_analyzer_flow():
    """Testa se o analisador bibliométrico processa as tabelas do SQLite corretamente."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()
    
    analyzer = BibliometricAnalyzer()
    
    # Testa se os métodos retornam DataFrames ou dicionários estruturados mesmo com base vazia
    temporal = analyzer.temporal_evolution()
    assert "total_preprints" in temporal.columns or temporal.empty
    
    compliance = analyzer.open_science_compliance()
    assert "orcid_adoption_rate_percent" in compliance
    
    edges = analyzer.generate_coauthorship_network_edges()
    assert "source" in edges.columns
    assert "target" in edges.columns