from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configurações de conexão com o banco de dados MySQL
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Incrivel10?',
    'database': 'todolist'
}

# ---------------------------------------------------------------------
# Funções auxiliares de banco de dados
# ---------------------------------------------------------------------

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

def get_all_tasks():
    """Retorna todas as tarefas do banco de dados."""
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)  # dictionary=True retorna resultado em formato de dicionário
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas

def get_task_by_nome(nome_tarefa):
    """Retorna uma única tarefa pelo nome."""
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE nome_tarefa = %s"
    cursor.execute(query, (nome_tarefa,))
    tarefa = cursor.fetchone()
    cursor.close()
    conn.close()
    return tarefa

def create_task(nome, descricao, prioridade, categoria):
    """Cria uma nova tarefa no banco de dados."""
    conn = criar_conexao()
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

def remove_task_by_nome(nome_tarefa):
    """Remove uma tarefa pelo nome."""
    conn = criar_conexao()
    cursor = conn.cursor()
    query = "DELETE FROM tasks WHERE nome_tarefa = %s"
    cursor.execute(query, (nome_tarefa,))
    rows_affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return rows_affected > 0  # Se afetou alguma linha, retorna True

def marcar_concluida(nome_tarefa):
    """Marca uma tarefa como concluída (status_tarefa=True)."""
    conn = criar_conexao()
    cursor = conn.cursor()
    query = """
        UPDATE tasks
        SET status_tarefa = TRUE
        WHERE nome_tarefa = %s
    """
    cursor.execute(query, (nome_tarefa,))
    rows_affected = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return rows_affected > 0

def get_tasks_by_prioridade(prioridade):
    """Retorna as tarefas filtradas por prioridade."""
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE prioridade = %s"
    cursor.execute(query, (prioridade,))
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas

def get_tasks_by_categoria(categoria):
    """Retorna as tarefas filtradas por categoria."""
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM tasks WHERE categoria = %s"
    cursor.execute(query, (categoria,))
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas

# ---------------------------------------------------------------------
# Rotas da API
# ---------------------------------------------------------------------

@app.route('/tarefas', methods=['GET'])
def rota_listar_tarefas():
    tarefas = get_all_tasks()
    return jsonify(tarefas), 200

@app.route('/tarefas', methods=['POST'])
def rota_adicionar_tarefa():
    try:
        # Logando a chegada da requisição
        app.logger.info("Recebido POST em /tarefas.")

        dados = request.json
        app.logger.info("JSON recebido: %s", dados)

        # Verifica se veio tudo que precisa
        if not all(chave in dados for chave in ["nome", "descricao", "prioridade", "categoria"]):
            app.logger.warning("Dados incompletos: %s", dados)
            return jsonify({"erro": "Dados incompletos para criar a tarefa"}), 400

        # Insere no banco
        create_task(
            nome=dados["nome"],
            descricao=dados["descricao"],
            prioridade=dados["prioridade"],
            categoria=dados["categoria"]
        )
        app.logger.info("Tarefa criada com sucesso: %s", dados["nome"])

        return jsonify({"mensagem": "Tarefa adicionada com sucesso!"}), 201

    except Exception as e:
        # Loga erro completo no console
        app.logger.error("Erro ao criar tarefa: %s", e, exc_info=True)
        return jsonify({"erro": str(e)}), 500


@app.route('/tarefas/<string:nome_tarefa>', methods=['DELETE'])
def rota_remover_tarefa(nome_tarefa):
    # Remove pelo nome
    removida = remove_task_by_nome(nome_tarefa)
    if removida:
        return jsonify({"mensagem": f"Tarefa '{nome_tarefa}' removida com sucesso."}), 200
    else:
        return jsonify({"erro": f"Tarefa '{nome_tarefa}' não encontrada."}), 404

@app.route('/tarefas/<string:nome_tarefa>/concluir', methods=['PUT'])
def rota_marcar_concluida(nome_tarefa):
    concluida = marcar_concluida(nome_tarefa)
    if concluida:
        return jsonify({"mensagem": f"Tarefa '{nome_tarefa}' marcada como concluída!"}), 200
    else:
        return jsonify({"erro": f"Tarefa '{nome_tarefa}' não encontrada."}), 404

@app.route('/tarefas/prioridade/<string:prioridade>', methods=['GET'])
def rota_exibir_por_prioridade(prioridade):
    filtradas = get_tasks_by_prioridade(prioridade)
    if filtradas:
        return jsonify(filtradas), 200
    else:
        return jsonify({"mensagem": f"Nenhuma tarefa encontrada com prioridade '{prioridade}'."}), 200

@app.route('/tarefas/categoria/<string:categoria>', methods=['GET'])
def rota_exibir_por_categoria(categoria):
    filtradas = get_tasks_by_categoria(categoria)
    if filtradas:
        return jsonify(filtradas), 200
    else:
        return jsonify({"mensagem": f"Nenhuma tarefa encontrada na categoria '{categoria}'."}), 200

if __name__ == '__main__':
    app.run(debug=True)
