import customtkinter as ctk
from datetime import date

from repositories.habit_repository import list_habits, create_habit, delete_habit
from services.habit_service import mark_habit


class HabitsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F172A")
        self.build()

    def build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="Hábitos",
            font=("Segoe UI", 32, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(side="left")

        add_button = ctk.CTkButton(
            header,
            text="+ Novo hábito",
            width=140,
            command=self.open_create_modal
        )
        add_button.pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#111827",
            corner_radius=18
        )
        self.list_frame.pack(fill="both", expand=True, pady=(24, 0))

        self.render_habits()

    def render_habits(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        habits = list_habits()

        for habit in habits:
            habit_id = habit[0]
            name = habit[1]
            description = habit[2]
            start_date = habit[3]
            current_streak = habit[4]
            best_streak = habit[5]
            active = habit[6]

            card = ctk.CTkFrame(self.list_frame, fg_color="#1E293B", corner_radius=16)
            card.pack(fill="x", padx=16, pady=10)

            info = ctk.CTkLabel(
                card,
                text=f"{name}\n{description or ''}\nInício: {start_date} | Streak: {current_streak} | Melhor: {best_streak} | Ativo: {active}",
                justify="left",
                font=("Segoe UI", 15),
                text_color="#F8FAFC"
            )
            info.pack(side="left", padx=18, pady=16)

            delete_button = ctk.CTkButton(
                card,
                text="Apagar",
                width=90,
                fg_color="#7F1D1D",
                hover_color="#991B1B",
                command=lambda hid=habit_id: self.remove_habit(hid)
            )
            delete_button.pack(side="right", padx=10)

            done_button = ctk.CTkButton(
                card,
                text="Feito hoje",
                width=110,
                command=lambda hid=habit_id: self.complete_habit(hid)
            )
            done_button.pack(side="right", padx=10)

    def open_create_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Novo hábito")
        modal.geometry("420x360")
        modal.configure(fg_color="#0F172A")
        modal.grab_set()

        name_entry = ctk.CTkEntry(modal, placeholder_text="Nome do hábito")
        name_entry.pack(fill="x", padx=24, pady=(32, 12))

        description_entry = ctk.CTkEntry(modal, placeholder_text="Descrição")
        description_entry.pack(fill="x", padx=24, pady=12)

        date_entry = ctk.CTkEntry(modal, placeholder_text="Data de início YYYY-MM-DD")
        date_entry.insert(0, str(date.today()))
        date_entry.pack(fill="x", padx=24, pady=12)

        def save():
            name = name_entry.get()
            description = description_entry.get()
            start_date = date.fromisoformat(date_entry.get())

            habit_id = create_habit(name, description, start_date)
            mark_habit(habit_id, True, start_date)

            modal.destroy()
            self.render_habits()

        save_button = ctk.CTkButton(modal, text="Salvar", command=save)
        save_button.pack(fill="x", padx=24, pady=24)

    def complete_habit(self, habit_id):
        mark_habit(habit_id, True)
        self.render_habits()

    def remove_habit(self, habit_id):
        delete_habit(habit_id)
        self.render_habits()