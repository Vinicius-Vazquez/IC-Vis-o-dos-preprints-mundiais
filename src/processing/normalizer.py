from unidecode import unidecode

class PreprintNormalizer:
    """Responsável por limpar, normalizar e mapear os metadados dos preprints."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Remove acentos, converte para minúsculas e remove espaços excedentes."""
        if not text:
            return ""
        return unidecode(text).strip().lower()

    @staticmethod
    def map_to_cnpq_area(concepts: list) -> str:
        """
        Mapeia os conceitos/tópicos retornados pela OpenAlex
        para as Grandes Áreas do Conhecimento do CNPq.
        """
        if not concepts:
            return "Multidisciplinar / Outras"
            
        # Analisa o primeiro conceito principal fornecido pela API
        top_concept = concepts[0].get("display_name", "").lower() if isinstance(concepts[0], dict) else str(concepts[0]).lower()
        
        if any(term in top_concept for term in ["computer", "software", "algorithm", "engineering", "math", "physics", "chemistry"]):
            return "Ciências Exatas e da Terra"
        elif any(term in top_concept for term in ["medicine", "health", "biology", "clinical", "biochem"]):
            return "Ciências da Saúde"
        elif any(term in top_concept for term in ["social", "sociology", "education", "economics", "law", "psycholog"]):
            return "Ciências Humanas / Sociais Aplicadas"
        elif any(term in top_concept for term in ["agriculture", "agronom", "forestry"]):
            return "Ciências Agrárias"
            
        return "Outras Áreas"

    def normalize_record(self, raw_data: dict) -> dict:
        """Aplica normalização completa em um registro bruto."""
        return {
            "id": raw_data.get("id"),
            "title": raw_data.get("title", "").strip(),
            "cnpq_area": self.map_to_cnpq_area(raw_data.get("concepts", [])),
            "has_orcid": int(any(auth.get("author", {}).get("orcid") is not None for auth in raw_data.get("authorships", [])))
        }