import re
from unidecode import unidecode

class PreprintNormalizer:
    """Responsável por limpar, normalizar e mapear os dados brutos da OpenAlex."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Remove acentos e converte para minúsculas para padronização básica
        return unidecode(text).strip().lower()

    @staticmethod
    def map_to_cnpq_area(openalex_concepts: list) -> str:
        """
        Mapeia conceitos/tópicos da OpenAlex para as Grandes Áreas do CNPq.
        (Ajustável conforme o dicionário de mapeamento do seu escopo de pesquisa).
        """
        if not openalex_concepts:
            str_area = "Multidisciplinar"
            return str_area
            
        # Exemplo simplificado de mapeamento baseado nos campos da OpenAlex
        top_concept = openalex_concepts[0].get("display_name", "").lower()
        
        if any(term in top_concept for term in ["computer", "software", "algorithm", "computational"]):
            return "Ciências Exatas e da Terra"
        elif any(term in top_concept for term in ["medicine", "health", "biolog", "clinic"]):
            return "Ciências da Saúde"
        elif any(term in top_concept for term in ["social", "sociolog", "educat", "econo"]):
            return "Ciências Humanas / Sociais Aplicadas"
        
        return "Outras Áreas"

    def normalize_work(self, raw_work: dict) -> dict:
        """Transforma um registro bruto da OpenAlex em um dicionário limpo para inserção."""
        authors = [
            {
                "author_id": author.get("author", {}).get("id"),
                "name": author.get("author", {}).get("display_name"),
                "orcid": author.get("author", {}).get("orcid"),
                "institution": author.get("institutions", [{}])[0].get("display_name") if author.get("institutions") else None
            }
            for author in raw_work.get("authorships", [])
        ]

        normalized = {
            "id": raw_work.get("id"),
            "doi": raw_work.get("doi"),
            "title": raw_work.get("title"),
            "publication_date": raw_work.get("publication_date"),
            "year": raw_work.get("publication_year"),
            "type": raw_work.get("type"),
            "cnpq_area": self.map_to_cnpq_area(raw_work.get("concepts", [])),
            "authors": authors,
            "has_orcid": any(a["orcid"] is not None for a in authors)
        }
        return normalized