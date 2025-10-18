"""
Script de Inicialização do Banco de Dados
Execute este arquivo após configurar o .env
"""

import sys
from core.database import DatabaseManager


def main():
    print("=" * 60)
    print("SmashMetrics - Inicialização do Banco de Dados")
    print("=" * 60)
    print()

    try:
        print("Conectando ao PostgreSQL...")
        db = DatabaseManager()
        print("✓ Conexão estabelecida com sucesso!")
        print()

        print("Criando tabelas...")
        db.create_tables()
        print("✓ Tabelas criadas com sucesso!")
        print()

        print("=" * 60)
        print("Banco de dados inicializado com sucesso!")
        print("=" * 60)
        print()
        print("Você pode agora executar a aplicação:")
        print("  python main.py")
        print()

        return 0

    except ConnectionError as e:
        print("✗ Erro de conexão com o banco de dados!")
        print()
        print("Possíveis causas:")
        print("1. PostgreSQL não está rodando")
        print("2. Credenciais incorretas no arquivo .env")
        print("3. Banco de dados não foi criado")
        print()
        print(f"Detalhes do erro: {e}")
        print()
        print("Consulte o arquivo SETUP.md para instruções detalhadas.")
        return 1

    except Exception as e:
        print("✗ Erro inesperado!")
        print(f"Detalhes: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())