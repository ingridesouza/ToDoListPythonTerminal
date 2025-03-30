import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'Incrivel10?',
            'database': 'todolist'
        }
    
    def criar_conexao(self):
        return mysql.connector.connect(**self.config)

class TaskModel:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        conn = self.db.criar_conexao()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks"
        cursor.execute(query)
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return tarefas

    def get_by_name(self, nome_tarefa):
        conn = self.db.criar_conexao()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE nome_tarefa = %s"
        cursor.execute(query, (nome_tarefa,))
        tarefa = cursor.fetchone()
        cursor.close()
        conn.close()
        return tarefa

    def create(self, nome, descricao, prioridade, categoria):
        conn = self.db.criar_conexao()
        cursor = conn.cursor()
        query = """
            INSERT INTO tasks (nome_tarefa, descricao, prioridade, categoria, status_tarefa)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (nome, descricao, prioridade, categoria, False)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()

    def remove(self, nome_tarefa):
        conn = self.db.criar_conexao()
        cursor = conn.cursor()
        query = "DELETE FROM tasks WHERE nome_tarefa = %s"
        cursor.execute(query, (nome_tarefa,))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rows_affected > 0

    def mark_completed(self, nome_tarefa):
        conn = self.db.criar_conexao()
        cursor = conn.cursor()
        query = "UPDATE tasks SET status_tarefa = TRUE WHERE nome_tarefa = %s"
        cursor.execute(query, (nome_tarefa,))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rows_affected > 0

    def get_by_priority(self, prioridade):
        conn = self.db.criar_conexao()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE prioridade = %s"
        cursor.execute(query, (prioridade,))
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return tarefas

    def get_by_category(self, categoria):
        conn = self.db.criar_conexao()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tasks WHERE categoria = %s"
        cursor.execute(query, (categoria,))
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return tarefas