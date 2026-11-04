from src.database.connection import init_db
from src.ingestion.collector import PreprintCollector
from src.processing.metrics import BibliometricAnalyzer

def main():
    print("=" * 60)
    print(" PIPELINE DE ANÁLISE DE PREPRINTS (OPENALEX) - INICIAÇÃO CIENTÍFICA ")
    print("=" * 60)

    # 1. Inicializa o banco de dados e as tabelas
    print("\n[1/4] Inicializando banco de dados SQLite (Modo WAL)...")
    init_db()

    # 2. Executa a coleta de amostra
    print("\n[2/4] Executando coleta de preprints da API OpenAlex...")
    collector = PreprintCollector()
    collector.run_sample_collection(max_records=10) # Amostra de teste ajustada

    # 3. Processa métricas e indicadores bibliométricos
    print("\n[3/4] Processando indicadores bibliométricos e redes...")
    analyzer = BibliometricAnalyzer()
    
    temporal_df = analyzer.temporal_evolution()
    cnpq_df = analyzer.cnpq_distribution()
    compliance = analyzer.open_science_compliance()
    edges_df = analyzer.generate_coauthorship_network_edges()

    # 4. Exibe os resultados consolidados no terminal
    print("\n[4/4] Relatório de Indicadores Cientométricos:")
    print("-" * 50)
    print(f"Total de registros analisados: {compliance.get('total', 0)}")
    print(f"Preprints com autores possuidores de ORCID: {compliance.get('preprints_with_orcid', 0)}")
    print(f"Taxa de adesão à Ciência Aberta (ORCID): {compliance.get('orcid_adoption_rate_percent', 0.0)}%")
    print("-" * 50)
    
    print("\nDistribuição por Grandes Áreas do CNPq:")
    if not cnpq_df.empty:
        print(cnpq_df.to_string(index=False))
    else:
        print("Nenhum dado categorizado na amostra atual.")

    print("\nArestas de Coautoria Geradas (Rede):", len(edges_df))
    print("=" * 60)
    print(" Pipeline executado com sucesso!")
    print("=" * 60)

if __name__ == "__main__":
    main()