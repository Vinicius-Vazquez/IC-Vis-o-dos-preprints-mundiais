import pandas as pd
from collections import Counter
import itertools

class BibliometricAnalyzer:
    """Calcula indicadores cientométricos e gera estruturas para redes de coautoria."""

    def __init__(self, df_works: pd.DataFrame):
        self.df = df_works

    def temporal_evolution(self) -> pd.DataFrame:
        """Calcula a evolução temporal da adoção de preprints (Objetivo Específico)."""
        if self.df.empty or "year" not in self.df.columns:
            return pd.DataFrame()
        return self.df.groupby("year").size().reset_index(name="total_preprints")

    def cnpq_distribution(self) -> pd.DataFrame:
        """Mapeia as áreas do conhecimento mais representativas (Objetivo Específico)."""
        if self.df.empty or "cnpq_area" not in self.df.columns:
            return pd.DataFrame()
        return self.df["cnpq_area"].value_counts().reset_index(name="quantidade")

    def open_science_compliance(self) -> dict:
        """Verifica a adesão a práticas de Ciência Aberta, como o uso do ORCID."""
        if self.df.empty or "has_orcid" not in self.df.columns:
            return {"total": 0, "with_orcid": 0, "percentage": 0.0}
        
        total = len(self.df)
        with_orcid = int(self.df["has_orcid"].sum())
        percentage = (with_orcid / total * 100) if total > 0 else 0.0
        
        return {
            "total_analysed": total,
            "authors_with_orcid": with_orcid,
            "orcid_adoption_rate_percent": round(percentage, 2)
        }

    def generate_coauthorship_network(self) -> pd.DataFrame:
        """Gera pares de coautoria para análise de redes (compatível com Gephi/VOSviewer)."""
        edges = []
        for authors_list in self.df.dropna(subset=["authors"])["authors"]:
            if isinstance(authors_list, list) and len(authors_list) > 1:
                names = [a["name"] for a in authors_list if a.get("name")]
                # Cria combinações de pares de autores no mesmo preprint
                for source, target in itertools.combinations(names, 2):
                    edges.append({"source": source, "target": target})
        
        return pd.DataFrame(edges)