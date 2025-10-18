# teste_cruds.py
from core.database import DatabaseManager, SeguradoraCRUD, AnaliseCRUD

db = DatabaseManager()
db.create_tables()

# Testar Seguradora
seg_crud = SeguradoraCRUD(db)
seg_id = seg_crud.create(
    nome="Porto Seguro",
    cnpj="12.345.678/0001-90",
    telefone="(85) 3456-7890",
    email="contato@portoseguro.com.br"
)
print(f"Seguradora criada: ID {seg_id}")

# Testar Análise
ana_crud = AnaliseCRUD(db)
ana_id = ana_crud.create(
    titulo="Colisão Frontal - Teste",
    seguradora_id=seg_id,
    numero_sinistro="SIN-2024-001",
    segurado="João da Silva"
)
print(f"Análise criada: ID {ana_id}")

# Listar
seguradoras = seg_crud.read_all()
print(f"Total de seguradoras: {len(seguradoras)}")

analises = ana_crud.read_all()
print(f"Total de análises: {len(analises)}")

