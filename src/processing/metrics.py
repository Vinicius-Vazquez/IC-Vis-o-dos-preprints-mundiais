import pandas as pd
import itertools
from src.database.connection import get_db_connection

class BibliometricAnalyzer:
    """Calcula indicadores cientométricos e gera estruturas para análise de redes de coautoria."""

    def __init__(self):
        pass

    def load_data_from_db(self) -> pd.DataFrame:
        """Carrega os dados consolidados da tabela de preprints do SQLite para um DataFrame Pandas."""
        conn = get_db_connection()
        query = "SELECT id, doi, title, year, cnpq_area, has_orcid FROM preprints;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def load_authors_from_db(self) -> pd.DataFrame:
        """Carrega os dados de autoria para análise de redes."""
        conn = get_db_connection()
        query = "SELECT work_id, author_id, name, orcid, institution FROM authors;"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def temporal_evolution(self) -> pd.DataFrame:
        """Calcula a evolução temporal da adoção de preprints."""
        df = self.load_data_from_db()
        if df.empty or "year" not in df.columns:
            return pd.DataFrame(columns=["year", "total_preprints"])
        return df.groupby("year").size().reset_index(name="total_preprints").sort_values("year")

    def cnpq_distribution(self) -> pd.DataFrame:
        """Mapeia a distribuição da produção pelas Grandes Áreas do CNPq."""
        df = self.load_data_from_db()
        if df.empty or "cnpq_area" not in df.columns:
            return pd.DataFrame(columns=["cnpq_area", "quantidade"])
        return df["cnpq_area"].value_counts().reset_index(name="quantidade")

    def open_science_compliance(self) -> dict:
        """Calcula a taxa de adoção de práticas de Ciência Aberta (uso de ORCID)."""
        df = self.load_data_from_db()
        if df.empty:
            return {"total": 0, "preprints_with_orcid": 0, "orcid_adoption_rate_percent": 0.0}
        
        total = len(df)
        with_orcid = int(df["has_orcid"].sum())
        percentage = (with_orcid / total * 100) if total > 0 else 0.0
        
        return {
            "total": total,
            "preprints_with_orcid": with_orcid,
            "orcid_adoption_rate_percent": round(percentage, 2)
        }

    def generate_coauthorship_network_edges(self) -> pd.DataFrame:
        """Gera pares de coautoria baseados nos preprints para análise de redes (VOSviewer/Gephi)."""
        authors_df = self.load_authors_from_db()
        if authors_df.empty:
            return pd.DataFrame(columns=["source", "target"])

        edges = []
        grouped = authors_df.groupby("work_id")["name"].apply(list)
        
        for authors_list in grouped:
            valid_names = [name for name in authors_list if name]
            if len(valid_names) > 1:
                for source, target in itertools.combinations(valid_names, 2):
                    edges.append({"source": source, "target": target})
        
        if not edges:
            return pd.DataFrame(columns=["source", "target"])
            
        edges_df = pd.DataFrame(edges)
        return edges_df.groupby(["source", "target"]).size().reset_index(name="weight")