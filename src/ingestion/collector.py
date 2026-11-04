import time
from src.ingestion.client import OpenAlexClient
from src.database.connection import get_db_connection
from src.config import CHECKPOINT_DIR

class PreprintCollector:
    """Coordenador do processo de ingestão, checkpointing e persistência de preprints."""
    
    def __init__(self):
        self.client = OpenAlexClient()
        self.checkpoint_file = CHECKPOINT_DIR / "cursor_checkpoint.txt"

    def _load_cursor(self) -> str:
        """Carrega o último cursor salvo para retomar a coleta em caso de interrupção."""
        if self.checkpoint_file.exists():
            return self.checkpoint_file.read_text(encoding="utf-8").strip()
        return "*"

    def _save_cursor(self, cursor: str):
        """Salva o cursor atual no disco de forma atômica."""
        self.checkpoint_file.write_text(cursor, encoding="utf-8")

    def run_sample_collection(self, max_records: int = 5):
        """
        Executa uma coleta de amostra limitada para testes de robustez e fluxo,
        armazenando os dados nas tabelas 'preprints' e 'authors'.
        """
        cursor = self._load_cursor()
        conn = get_db_connection()
        cursor_db = conn.cursor()
        
        collected_count = 0
        print(f"[INFO] Iniciando coleta de amostra (Meta: {max_records} registros)...")

        try:
            # Tenta buscar a primeira página com cursor "*"
            data = self.client.fetch_works(cursor=cursor, per_page=max_records)
            meta = data.get("meta", {})
            results = data.get("results", [])
            
            if not results:
                print("[AVISO] Nenhum resultado retornado. Tentando busca sem cursor (fallback para página 1)...")
                # Fallback caso o cursor exija chave e venha vazio
                import requests
                response = requests.get(
                    "https://api.openalex.org/works",
                    headers={"User-Agent": "mailto:vazquez@aluno.cefetmg.br"},
                    params={"filter": "type:preprint", "per_page": max_records}
                )
                if response.status_code == 200:
                    results = response.json().get("results", [])

            for work in results:
                work_id = work.get("id")
                doi = work.get("doi")
                title = work.get("title")
                pub_date = work.get("publication_date")
                year = work.get("publication_year")
                work_type = work.get("type")
                
                # Inserção do preprint principal
                cursor_db.execute("""
                    INSERT OR IGNORE INTO preprints (id, doi, title, publication_date, year, type, cnpq_area, has_orcid)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (work_id, doi, title, pub_date, year, work_type, "Não classificado", 0))
                
                # Inserção dos autores associados
                authorships = work.get("authorships", [])
                has_orcid_flag = 0
                for auth in authorships:
                    author_info = auth.get("author", {})
                    author_id = author_info.get("id")
                    name = author_info.get("display_name")
                    orcid = author_info.get("orcid")
                    institution = auth.get("institutions", [{}])[0].get("display_name") if auth.get("institutions") else None
                    
                    if orcid:
                        has_orcid_flag = 1
                        
                    cursor_db.execute("""
                        INSERT INTO authors (work_id, author_id, name, orcid, institution)
                        VALUES (?, ?, ?, ?, ?)
                    """, (work_id, author_id, name, orcid, institution))
                
                # Atualiza o status de ORCID na tabela principal
                cursor_db.execute("""
                    UPDATE preprints SET has_orcid = ? WHERE id = ?
                """, (has_orcid_flag, work_id))
                
                collected_count += 1
                if collected_count >= max_records:
                    break
            
            conn.commit()
            print(f"[INFO] Coleta de amostra finalizada. Total processado: {collected_count} registros.")
                
        except Exception as e:
            print(f"[ERRO NO COLETOR] Ocorreu uma exceção: {e}")
            conn.rollback()
        finally:
            conn.close()