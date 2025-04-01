from typing import List, Optional
from produtos.produto import Presidiario  # Importa a classe de domínio
from produtos import produto_sql as sql # Importa as constantes SQL
from util import get_db_connection     # Importa o gerenciador de conexão
import sqlite3

class PresidiarioRepo:
    """
    Repositório para gerenciar operações CRUD para a entidade Presidiario no banco de dados.
    """
    def __init__(self):
        """Inicializa o repositório e garante que a tabela de presidiarios exista."""
        self._criar_tabela()

    def _criar_tabela(self):
        """Método privado para criar a tabela 'presidiarios' se ela não existir."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.CREATE_TABLE)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def adicionar(self, presidiario: Presidiario) -> Optional[int]:
        """
        Adiciona um novo presidiario ao banco de dados.
        Retorna o ID do presidiario inserido ou None em caso de erro.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.INSERT_PRESIDIARIO,
                               (presidiario.nome, str(presidiario.data_nascimento), presidiario.crime, presidiario.cela))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao adicionar presidiario: {e}")
            return None

    def obter(self, presidiario_id: int) -> Optional[Presidiario]:
        """
        Busca um presidiario no banco de dados pelo seu ID.
        Retorna um objeto Presidiario se encontrado, caso contrário, retorna None.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_PRESIDIARIO, (presidiario_id,))
                row = cursor.fetchone()
                if row:
                    return Presidiario(id=row[0], nome=row[1], data_nascimento=row[2], crime=row[3], cela=row[4])
                return None
        except sqlite3.Error as e:
            print(f"Erro ao obter presidiario {presidiario_id}: {e}")
            return None

    def obter_todos(self) -> List[Presidiario]:
        """
        Busca todos os presidiarios cadastrados no banco de dados.
        Retorna uma lista de objetos Presidiario.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_TODOS_PRESIDIARIOS)
                rows = cursor.fetchall()
                return [Presidiario(id=row[0], nome=row[1], data_nascimento=row[2], crime=row[3], cela=row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao obter todos os presidiarios: {e}")
            return []

    def atualizar(self, presidiario: Presidiario) -> bool:
        """
        Atualiza os dados de um presidiario existente no banco de dados.
        Retorna True se a atualização foi bem-sucedida, False caso contrário.
        """
        if presidiario.id is None:
            print("Erro: Presidiario sem ID não pode ser atualizado.")
            return False
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.UPDATE_PRESIDIARIO,
                               (presidiario.nome, str(presidiario.data_nascimento), presidiario.crime, presidiario.cela, presidiario.id))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar presidiario {presidiario.id}: {e}")
            return False

    def excluir(self, presidiario_id: int) -> bool:
        """
        Exclui um presidiario do banco de dados pelo seu ID.
        Retorna True se a exclusão foi bem-sucedida, False caso contrário.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.DELETE_PRESIDIARIO, (presidiario_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir presidiario {presidiario_id}: {e}")
            return False
