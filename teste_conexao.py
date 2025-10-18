# teste_conexao.py
from core.database import DatabaseManager

try:
    db = DatabaseManager()
    print("✓ Conexão com banco de dados estabelecida!")
except Exception as e:
    print(f"✗ Erro ao conectar: {e}")
