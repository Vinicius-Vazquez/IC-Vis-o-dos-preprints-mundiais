import os
import requests
from src.config import OPENALEX_BASE_URL, OPENALEX_EMAIL

class OpenAlexClient:
    """Cliente HTTP robusto para comunicação com a API OpenAlex."""
    
    def __init__(self, api_key: str = None):
        self.base_url = OPENALEX_BASE_URL
        self.api_key = api_key or os.getenv("OPENALEX_API_KEY")
        self.headers = {
            "User-Agent": f"mailto:{OPENALEX_EMAIL}"
        }

    def fetch_works(self, cursor: str = "*", per_page: int = 25) -> dict:
        """
        Busca uma página de preprints utilizando paginação.
        Se houver cursor e o OpenAlex exigir chave para cursor, podemos usar paginação por página se necessário.
        """
        params = {
            "filter": "type:preprint",
            "per_page": per_page,
            "cursor": cursor
        }
        
        # Se houver chave de API configurada, adiciona aos parâmetros
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print(f"[AVISO] O OpenAlex exige chave de API para cursor: {response.text}")
                return {}
            elif response.status_code == 429:
                print("[AVISO] Rate limit atingido (429).")
                return {}
            else:
                print(f"[ERRO] Falha na API OpenAlex: Status {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"[ERRO DE CONEXÃO] Ocorreu um erro ao acessar a API: {e}")
            return {}