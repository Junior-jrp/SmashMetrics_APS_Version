"""
Gerenciador de Banco de Dados PostgreSQL
CRUDs: Seguradoras e Análises
"""

import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class DatabaseManager:
    """Gerenciador de conexão com PostgreSQL"""

    def __init__(self):
        self.connection_pool = None
        self.init_connection_pool()

    def init_connection_pool(self):
        """Inicializa o pool de conexões"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'smashmetrics'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', '')
            )
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    def get_connection(self):
        """Obtém uma conexão do pool"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        raise ConnectionError("Pool de conexões não inicializado")

    def return_connection(self, conn):
        """Retorna conexão ao pool"""
        if self.connection_pool:
            self.connection_pool.putconn(conn)

    def close_all_connections(self):
        """Fecha todas as conexões do pool"""
        if self.connection_pool:
            self.connection_pool.closeall()

    def create_tables(self):
        """Cria as tabelas no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Tabela de Seguradoras
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seguradoras (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    cnpj VARCHAR(18) UNIQUE,
                    telefone VARCHAR(20),
                    email VARCHAR(255),
                    endereco TEXT,
                    contato_responsavel VARCHAR(255),
                    observacoes TEXT,
                    ativo BOOLEAN DEFAULT TRUE,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabela de Análises
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analises (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    seguradora_id INTEGER REFERENCES seguradoras(id) ON DELETE SET NULL,
                    numero_sinistro VARCHAR(100),
                    data_acidente DATE,
                    segurado VARCHAR(255),
                    numero_apolice VARCHAR(100),
                    local_colisao TEXT,
                    tipo_colisao VARCHAR(100),
                    deformacao_cm DECIMAL(10, 2),
                    velocidade_kmh DECIMAL(10, 2),
                    energia_joules DECIMAL(15, 2),
                    massa_veiculo DECIMAL(10, 2),
                    caminho_imagem TEXT,
                    scale_factor DECIMAL(10, 6),
                    observacoes TEXT,
                    status VARCHAR(50) DEFAULT 'Em andamento',
                    data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Índices para melhor performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analises_seguradora 
                ON analises(seguradora_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analises_status 
                ON analises(status)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_analises_data 
                ON analises(data_analise)
            """)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.return_connection(conn)


class SeguradoraCRUD:
    """CRUD para Seguradoras"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create(self, nome: str, cnpj: Optional[str] = None,
               telefone: Optional[str] = None, email: Optional[str] = None,
               endereco: Optional[str] = None, contato_responsavel: Optional[str] = None,
               observacoes: Optional[str] = None) -> int:
        """Cria nova seguradora"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO seguradoras 
                (nome, cnpj, telefone, email, endereco, contato_responsavel, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (nome, cnpj, telefone, email, endereco, contato_responsavel, observacoes))

            seguradora_id = cursor.fetchone()[0]
            conn.commit()
            return seguradora_id

        except psycopg2.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"CNPJ já cadastrado: {e}")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def read(self, seguradora_id: int) -> Optional[Dict[str, Any]]:
        """Busca seguradora por ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT * FROM seguradoras WHERE id = %s
            """, (seguradora_id,))

            result = cursor.fetchone()
            return dict(result) if result else None

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def read_all(self, apenas_ativas: bool = True) -> List[Dict[str, Any]]:
        """Lista todas as seguradoras"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            if apenas_ativas:
                cursor.execute("""
                    SELECT * FROM seguradoras 
                    WHERE ativo = TRUE 
                    ORDER BY nome
                """)
            else:
                cursor.execute("""
                    SELECT * FROM seguradoras 
                    ORDER BY nome
                """)

            results = cursor.fetchall()
            return [dict(row) for row in results]

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def update(self, seguradora_id: int, **kwargs) -> bool:
        """Atualiza seguradora"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        campos_permitidos = ['nome', 'cnpj', 'telefone', 'email', 'endereco',
                            'contato_responsavel', 'observacoes', 'ativo']

        campos = []
        valores = []

        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)

        if not campos:
            return False

        # Adiciona atualização de timestamp
        campos.append("data_atualizacao = CURRENT_TIMESTAMP")
        valores.append(seguradora_id)

        query = f"UPDATE seguradoras SET {', '.join(campos)} WHERE id = %s"

        try:
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def delete(self, seguradora_id: int, soft_delete: bool = True) -> bool:
        """
        Remove seguradora
        soft_delete=True: apenas marca como inativa
        soft_delete=False: remove permanentemente (só se não houver análises)
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            if soft_delete:
                cursor.execute("""
                    UPDATE seguradoras SET ativo = FALSE WHERE id = %s
                """, (seguradora_id,))
            else:
                # Verifica se há análises vinculadas
                cursor.execute("""
                    SELECT COUNT(*) FROM analises WHERE seguradora_id = %s
                """, (seguradora_id,))

                count = cursor.fetchone()[0]
                if count > 0:
                    raise ValueError(
                        f"Não é possível excluir. Existem {count} análise(s) vinculada(s)."
                    )

                cursor.execute("""
                    DELETE FROM seguradoras WHERE id = %s
                """, (seguradora_id,))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def search(self, termo: str) -> List[Dict[str, Any]]:
        """Busca seguradoras por nome, CNPJ ou email"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT * FROM seguradoras 
                WHERE (nome ILIKE %s OR cnpj ILIKE %s OR email ILIKE %s)
                AND ativo = TRUE
                ORDER BY nome
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            results = cursor.fetchall()
            return [dict(row) for row in results]

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def get_statistics(self, seguradora_id: int) -> Dict[str, Any]:
        """Retorna estatísticas de uma seguradora"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_analises,
                    COUNT(CASE WHEN status = 'Concluída' THEN 1 END) as analises_concluidas,
                    COUNT(CASE WHEN status = 'Em andamento' THEN 1 END) as analises_andamento,
                    AVG(velocidade_kmh) as velocidade_media
                FROM analises 
                WHERE seguradora_id = %s
            """, (seguradora_id,))

            result = cursor.fetchone()
            return dict(result) if result else {}

        finally:
            cursor.close()
            self.db.return_connection(conn)


class AnaliseCRUD:
    """CRUD para Análises"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create(self, titulo: str, seguradora_id: Optional[int] = None,
               numero_sinistro: Optional[str] = None, data_acidente: Optional[str] = None,
               segurado: Optional[str] = None, numero_apolice: Optional[str] = None,
               local_colisao: Optional[str] = None, tipo_colisao: Optional[str] = None,
               deformacao_cm: Optional[float] = None, velocidade_kmh: Optional[float] = None,
               energia_joules: Optional[float] = None, massa_veiculo: Optional[float] = None,
               caminho_imagem: Optional[str] = None, scale_factor: Optional[float] = None,
               observacoes: Optional[str] = None, status: str = "Em andamento") -> int:
        """Cria nova análise"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO analises 
                (titulo, seguradora_id, numero_sinistro, data_acidente, segurado, 
                numero_apolice, local_colisao, tipo_colisao, deformacao_cm, 
                velocidade_kmh, energia_joules, massa_veiculo, caminho_imagem, 
                scale_factor, observacoes, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (titulo, seguradora_id, numero_sinistro, data_acidente, segurado,
                  numero_apolice, local_colisao, tipo_colisao, deformacao_cm,
                  velocidade_kmh, energia_joules, massa_veiculo, caminho_imagem,
                  scale_factor, observacoes, status))

            analise_id = cursor.fetchone()[0]
            conn.commit()
            return analise_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def read(self, analise_id: int) -> Optional[Dict[str, Any]]:
        """Busca análise por ID com dados da seguradora"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT a.*, 
                       s.nome as seguradora_nome,
                       s.cnpj as seguradora_cnpj
                FROM analises a
                LEFT JOIN seguradoras s ON a.seguradora_id = s.id
                WHERE a.id = %s
            """, (analise_id,))

            result = cursor.fetchone()
            return dict(result) if result else None

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def read_all(self, filtro_status: Optional[str] = None,
                 filtro_seguradora: Optional[int] = None,
                 limite: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista todas as análises com filtros opcionais"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            query = """
                SELECT a.*, 
                       s.nome as seguradora_nome
                FROM analises a
                LEFT JOIN seguradoras s ON a.seguradora_id = s.id
                WHERE 1=1
            """
            params = []

            if filtro_status:
                query += " AND a.status = %s"
                params.append(filtro_status)

            if filtro_seguradora:
                query += " AND a.seguradora_id = %s"
                params.append(filtro_seguradora)

            query += " ORDER BY a.data_analise DESC"

            if limite:
                query += " LIMIT %s"
                params.append(limite)

            cursor.execute(query, params)
            results = cursor.fetchall()
            return [dict(row) for row in results]

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def update(self, analise_id: int, **kwargs) -> bool:
        """Atualiza análise"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        campos_permitidos = [
            'titulo', 'seguradora_id', 'numero_sinistro', 'data_acidente',
            'segurado', 'numero_apolice', 'local_colisao', 'tipo_colisao',
            'deformacao_cm', 'velocidade_kmh', 'energia_joules', 'massa_veiculo',
            'caminho_imagem', 'scale_factor', 'observacoes', 'status'
        ]

        campos = []
        valores = []

        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                campos.append(f"{campo} = %s")
                valores.append(valor)

        if not campos:
            return False

        # Adiciona atualização de timestamp
        campos.append("data_atualizacao = CURRENT_TIMESTAMP")
        valores.append(analise_id)

        query = f"UPDATE analises SET {', '.join(campos)} WHERE id = %s"

        try:
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def delete(self, analise_id: int) -> bool:
        """Remove análise permanentemente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM analises WHERE id = %s
            """, (analise_id,))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            self.db.return_connection(conn)

    def search(self, termo: str) -> List[Dict[str, Any]]:
        """Busca análises por título, sinistro, segurado ou local"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT a.*, 
                       s.nome as seguradora_nome
                FROM analises a
                LEFT JOIN seguradoras s ON a.seguradora_id = s.id
                WHERE (a.titulo ILIKE %s 
                   OR a.numero_sinistro ILIKE %s 
                   OR a.segurado ILIKE %s
                   OR a.local_colisao ILIKE %s
                   OR s.nome ILIKE %s)
                ORDER BY a.data_analise DESC
            """, (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%"))

            results = cursor.fetchall()
            return [dict(row) for row in results]

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais das análises"""
        conn = self.db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_analises,
                    COUNT(CASE WHEN status = 'Concluída' THEN 1 END) as concluidas,
                    COUNT(CASE WHEN status = 'Em andamento' THEN 1 END) as em_andamento,
                    COUNT(CASE WHEN status = 'Arquivada' THEN 1 END) as arquivadas,
                    AVG(velocidade_kmh) as velocidade_media,
                    MAX(velocidade_kmh) as velocidade_maxima,
                    AVG(deformacao_cm) as deformacao_media
                FROM analises
            """)

            result = cursor.fetchone()
            return dict(result) if result else {}

        finally:
            cursor.close()
            self.db.return_connection(conn)

    def get_recent(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna as análises mais recentes"""
        return self.read_all(limite=limite)