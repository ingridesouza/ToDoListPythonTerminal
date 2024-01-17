def criar_tarefa(nome, descricao, prioridade, categoria, concluida=False):
    return {'Nome_Tarefa': nome,
            'Descricao_Tarefa': descricao,
            'Prioridade_Tarefa': prioridade,
            'Categoria_Tarefa': categoria,
            'Status_Tarefa': concluida}
    
#-----------------------------------------------------------------------
def adicionar_tarefa(lista_tarefas, tarefas):
    lista_tarefas.append(tarefas)
    print('Tarefa Adicionada!')

#-----------------------------------------------------------------------
    
def remover_tarefa(lista_tarefas, nome_excluir):
    for tarefa in lista_tarefas:
     if tarefa["Nome_tarefa"] == nome_excluir:
        tarefa.remove(nome_excluir)
        print(f"Tarefa '{nome_excluir}' removida com sucesso.")
        return
    print(f"Tarefa '{nome_excluir}' não encontrada na lista.")

#-----------------------------------------------------------------------
# Função para listar tarefas
def listar_tarefas(lista_tarefas):
    # o 'i' é o indice do item
    # para cada tarefa na lista de tarefas, pega cada tarefa e indice da lista de tarefas
    for i, tarefa in enumerate(lista_tarefas, start=1):
        print(f"{i}. {tarefa['Nome_Tarefa']} - {tarefa['Descricao_Tarefa']} - {tarefa['Prioridade_Tarefa']} - {tarefa['Categoria_Tarefa']} - Concluída: {tarefa['Status_Tarefa']}")
        print('-'*50)

#-----------------------------------------------------------------------
# Função para marcar tarefa como concluída
def marcar_como_concluida(lista_tarefas, nome_tarefa):
    # Itera sobre cada tarefa na lista de tarefas
    for tarefa in lista_tarefas:
        # Verifica se o nome da tarefa atual é igual ao nome da tarefa que queremos marcar como concluída
        if tarefa["Nome_Tarefa"] == nome_tarefa:
            # Marca a tarefa como concluída, alterando o valor da chave "Status_Tarefa" para True
            tarefa["Status_Tarefa"] = True
            # Imprime uma mensagem indicando que a tarefa foi marcada como concluída
            # print(f"Tarefa '{nome_tarefa}' marcada como concluída!")
            print(f"\x1b[9m Tarefa '{nome_tarefa}' marcada como concluída! \x1b[0m")
            # Retorna imediatamente após marcar a tarefa como concluída
            return
    # Se o loop não encontrar a tarefa, imprime uma mensagem indicando que a tarefa não foi encontrada
    print(f"Tarefa '{nome_tarefa}' não encontrada.")

#-----------------------------------------------------------------------
# Função para exibir tarefas por prioridade
def exibir_por_prioridade(lista_tarefas, prioridade):
    # Cria uma lista de tarefas filtradas pela prioridade fornecida
    tarefas_filtradas = [tarefa for tarefa in lista_tarefas if tarefa["Prioridade_Tarefa"] == prioridade]

    # Verifica se existem tarefas filtradas com a prioridade especificada
    if tarefas_filtradas:
        # Imprime um cabeçalho indicando as tarefas com a prioridade fornecida
        print(f"Tarefas com prioridade {prioridade}:")
        # Chama a função listar_tarefas para imprimir as tarefas filtradas
        listar_tarefas(tarefas_filtradas)
    else:
        # Se não houver tarefas filtradas, imprime uma mensagem informando que nenhuma tarefa foi encontrada com a prioridade especificada
        print(f"Nenhuma tarefa encontrada com prioridade {prioridade}.")

#---------------------------------------------------------------------
# Função para exibir tarefas por categoria
def exibir_por_categoria(lista_tarefas, categoria):
    # Filtra as tarefas na lista com base na categoria fornecida
    tarefas_filtradas = [tarefa for tarefa in lista_tarefas if tarefa["Categoria_Tarefa"] == categoria]

    # Verifica se há tarefas na categoria filtrada
    if tarefas_filtradas:
        # Imprime o cabeçalho informando a categoria
        print(f"Tarefas na categoria {categoria}:")
        # Chama a função listar_tarefas para imprimir as tarefas filtradas
        listar_tarefas(tarefas_filtradas)
    else:
        # Se não houver tarefas na categoria, imprime uma mensagem informando
        print(f"Nenhuma tarefa encontrada na categoria {categoria}.")

