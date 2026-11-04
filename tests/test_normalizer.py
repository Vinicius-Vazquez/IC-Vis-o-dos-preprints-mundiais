from src.processing.normalizer import PreprintNormalizer

def test_clean_text():
    """Testa a limpeza e remoção de acentos de textos."""
    normalizer = PreprintNormalizer()
    assert normalizer.clean_text("  Ciência Aberta!  ") == "ciencia aberta!"

def test_cnpq_mapping():
    """Testa o mapeamento correto de conceitos para as Grandes Áreas do CNPq."""
    normalizer = PreprintNormalizer()
    
    concepts_exact = [{"display_name": "Computer Science"}]
    assert normalizer.map_to_cnpq_area(concepts_exact) == "Ciências Exatas e da Terra"
    
    concepts_health = [{"display_name": "Medicine"}]
    assert normalizer.map_to_cnpq_area(concepts_health) == "Ciências da Saúde"
    
    assert normalizer.map_to_cnpq_area([]) == "Multidisciplinar / Outras"