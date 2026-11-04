from src.ingestion.client import OpenAlexClient

def test_openalex_client_connection():
    """Testa se o cliente consegue realizar uma requisição básica e retornar metadados válidos."""
    client = OpenAlexClient()
    data = client.fetch_works(cursor="*", per_page=1)
    
    assert isinstance(data, dict), "A resposta da API deve ser um dicionário JSON."
    assert "meta" in data, "A resposta deve conter metadados de paginação ('meta')."
    assert "results" in data, "A resposta deve conter a lista de resultados ('results')."