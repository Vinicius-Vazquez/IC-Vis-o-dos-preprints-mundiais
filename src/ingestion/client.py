import requests
from src.config import OPENALEX_BASE_URL, OPENALEX_EMAIL

class OpenAlexClient:
    """Cliente HTTP robusto para comunicação com a API OpenAlex."""
    
    def __init__(self):
        self.base_url = OPENALEX_BASE_URL
        self.headers = {
            "User-Agent": f"mailto:{OPENALEX_EMAIL}"
        }

    def fetch_works(self, cursor: str = "*", per_page: int = 1) -> dict:
        """
        Busca uma página de preprints utilizando paginação por cursor
        e inserindo o e-mail no Polite Pool.
        """
        # Utiliza o tipo correto indicado pela documentação da OpenAlex
        params = {
            "filter": "type:preprint",
            "per_page": per_page,
            "cursor": cursor
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("[AVISO] Rate limit atingido (429).")
                return {}
            else:
                print(f"[ERRO] Falha na API OpenAlex: Status {response.status_code} - {response.text}")
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"[ERRO DE CONEXÃO] Ocorreu um erro ao acessar a API: {e}")
            return {}