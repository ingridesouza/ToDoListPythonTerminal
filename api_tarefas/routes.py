from flask import jsonify, request, render_template
from .models import TaskModel

task_model = TaskModel()

def init_routes(bp):
    # Rota raiz para evitar "Not Found"
    @bp.route('/')
    def index():
        return render_template('main.html')  # Certifique-se de ter este template

    # API de tarefas
    @bp.route('/tarefas', methods=['GET'])
    def list_tasks():
        tasks = task_model.get_all()
        return jsonify(tasks), 200

    @bp.route('/tarefas', methods=['POST'])
    def add_task():
        try:
            dados = request.json
            if not all(chave in dados for chave in ["nome", "descricao", "prioridade", "categoria"]):
                return jsonify({"erro": "Dados incompletos"}), 400

            task_model.create(
                nome=dados["nome"],
                descricao=dados["descricao"],
                prioridade=dados["prioridade"],
                categoria=dados["categoria"]
            )
            return jsonify({"mensagem": "Tarefa adicionada com sucesso!"}), 201

        except Exception as e:
            return jsonify({"erro": str(e)}), 500

    @bp.route('/tarefas/<string:nome_tarefa>', methods=['DELETE'])
    def remove_task(nome_tarefa):
        if task_model.remove(nome_tarefa):
            return jsonify({"mensagem": f"Tarefa '{nome_tarefa}' removida com sucesso."}), 200
        return jsonify({"erro": f"Tarefa '{nome_tarefa}' não encontrada."}), 404

    @bp.route('/tarefas/<string:nome_tarefa>/concluir', methods=['PUT'])
    def complete_task(nome_tarefa):
        if task_model.mark_completed(nome_tarefa):
            return jsonify({"mensagem": f"Tarefa '{nome_tarefa}' concluída!"}), 200
        return jsonify({"erro": f"Tarefa '{nome_tarefa}' não encontrada."}), 404

    @bp.route('/tarefas/prioridade/<string:prioridade>', methods=['GET'])
    def filter_by_priority(prioridade):
        tasks = task_model.get_by_priority(prioridade)
        return jsonify(tasks if tasks else {"mensagem": f"Nenhuma tarefa com prioridade '{prioridade}'"}), 200

    @bp.route('/tarefas/categoria/<string:categoria>', methods=['GET'])
    def filter_by_category(categoria):
        tasks = task_model.get_by_category(categoria)
        return jsonify(tasks if tasks else {"mensagem": f"Nenhuma tarefa na categoria '{categoria}'"}), 200