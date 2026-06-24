from datetime import date
from repositories.habit_repository import create_habit, list_habits, delete_habit
from repositories.goal_repository import create_goal, list_goals, update_goal_status, delete_goal
from services.habit_service import mark_habit


def show_menu():
    while True:
        print("\n===== GERENCIADOR DE METAS E HÁBITOS =====")
        print("1 - Criar hábito")
        print("2 - Listar hábitos")
        print("3 - Marcar hábito como feito hoje")
        print("4 - Marcar hábito como não feito hoje")
        print("5 - Apagar hábito")
        print("6 - Criar meta")
        print("7 - Listar metas")
        print("8 - Alterar status da meta")
        print("9 - Apagar meta")
        print("0 - Sair")

        option = input("\nEscolha: ")

        if option == "1":
            name = input("Nome do hábito: ")
            description = input("Descrição: ")
            start_date_input = input("Data de início YYYY-MM-DD: ")

            start_date = date.fromisoformat(start_date_input)

            habit_id = create_habit(name, description, start_date)

            mark_habit(habit_id, True, start_date)

            print(f"Hábito criado com ID {habit_id}")
        elif option == "2":
            habits = list_habits()

            print("\n--- HÁBITOS ---")
            for h in habits:
                print(
                    f"ID: {h[0]} | {h[1]} | Início: {h[3]} | "
                    f"Streak atual: {h[4]} | Melhor streak: {h[5]} | Ativo: {h[6]}"
                )

        elif option == "3":
            habit_id = int(input("ID do hábito: "))
            mark_habit(habit_id, True)
            print("Hábito marcado como feito hoje.")

        elif option == "4":
            habit_id = int(input("ID do hábito: "))
            mark_habit(habit_id, False)
            print("Hábito marcado como não feito hoje.")

        elif option == "5":
            habit_id = int(input("ID do hábito: "))
            delete_habit(habit_id)
            print("Hábito apagado.")

        elif option == "6":
            title = input("Título da meta: ")
            description = input("Descrição: ")
            deadline_input = input("Prazo YYYY-MM-DD ou vazio: ")

            deadline = date.fromisoformat(deadline_input) if deadline_input else None

            goal_id = create_goal(title, description, deadline)
            print(f"Meta criada com ID {goal_id}")

        elif option == "7":
            goals = list_goals()

            print("\n--- METAS ---")
            for g in goals:
                print(
                    f"ID: {g[0]} | {g[1]} | Status: {g[3]} | "
                    f"Criada em: {g[4]} | Prazo: {g[5]}"
                )

        elif option == "8":
            goal_id = int(input("ID da meta: "))
            status = input("Novo status ativa/concluida/pausada: ")
            update_goal_status(goal_id, status)
            print("Status atualizado.")

        elif option == "9":
            goal_id = int(input("ID da meta: "))
            delete_goal(goal_id)
            print("Meta apagada.")

        elif option == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")