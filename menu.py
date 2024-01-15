from funcoes import *
from bancoDados import *

while True:
        print('''
              1- Adicionar uma tarefa
              2- Listar tarefas
              3- Marcar tarefa como concluída
              4- Exibir tarefas por prioridade
              5- Exibir tarefas por categoria
              6- Remover Tarefa
              7- Sair
              ''')
        escolha = input("Escolha uma opção: ")

        match escolha:
            case "1":
                nome = input("Digite o nome da tarefa: ")
                descricao = input("Digite a descrição da tarefa: ")
                prioridade = input("Digite a prioridade da tarefa: ")
                categoria = input("Digite a categoria da tarefa: ")
                nova_tarefa = criar_tarefa(nome, descricao, prioridade, categoria)
                adicionar_tarefa(lista_tarefas, nova_tarefa)

            case "2":
                listar_tarefas(lista_tarefas)

            case "3":
                nome_tarefa = input("Digite o nome da tarefa a ser marcada como concluída: ")
                marcar_como_concluida(lista_tarefas, nome_tarefa)

            case "4":
                prioridade = input("Digite a prioridade para filtrar as tarefas: ")
                exibir_por_prioridade(lista_tarefas, prioridade)

            case "5":
                categoria = input("Digite a categoria para filtrar as tarefas: ")
                exibir_por_categoria(lista_tarefas, categoria)

            case "6":
                nome_excluir = input("Digite o nome da tarefa que deseja remover: ")
                remover_tarefa(lista_tarefas, nome_excluir)

            case "7":
                print("Saindo...")
                break

            case _:
                print("Opção inválida. Tente novamente.")