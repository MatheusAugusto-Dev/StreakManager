import customtkinter as ctk
from datetime import date

from repositories.goal_repository import (
    list_goals,
    create_goal,
    delete_goal,
    update_goal_status
)


class GoalsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F172A")
        self.build()

    def build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="Metas",
            font=("Segoe UI", 32, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(side="left")

        add_button = ctk.CTkButton(
            header,
            text="+ Nova meta",
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

        self.render_goals()

    def render_goals(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        goals = list_goals()

        for goal in goals:
            goal_id = goal[0]
            title = goal[1]
            description = goal[2]
            status = goal[3]
            created_at = goal[4]
            deadline = goal[5]

            card = ctk.CTkFrame(self.list_frame, fg_color="#1E293B", corner_radius=16)
            card.pack(fill="x", padx=16, pady=10)

            info = ctk.CTkLabel(
                card,
                text=f"{title}\n{description or ''}\nStatus: {status} | Criada: {created_at} | Prazo: {deadline}",
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
                command=lambda gid=goal_id: self.remove_goal(gid)
            )
            delete_button.pack(side="right", padx=10)

            conclude_button = ctk.CTkButton(
                card,
                text="Concluir",
                width=100,
                command=lambda gid=goal_id: self.change_status(gid, "concluida")
            )
            conclude_button.pack(side="right", padx=10)

            pause_button = ctk.CTkButton(
                card,
                text="Pausar",
                width=90,
                fg_color="#92400E",
                hover_color="#B45309",
                command=lambda gid=goal_id: self.change_status(gid, "pausada")
            )
            pause_button.pack(side="right", padx=10)

    def open_create_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Nova meta")
        modal.geometry("420x360")
        modal.configure(fg_color="#0F172A")
        modal.grab_set()

        title_entry = ctk.CTkEntry(modal, placeholder_text="Título da meta")
        title_entry.pack(fill="x", padx=24, pady=(32, 12))

        description_entry = ctk.CTkEntry(modal, placeholder_text="Descrição")
        description_entry.pack(fill="x", padx=24, pady=12)

        deadline_entry = ctk.CTkEntry(modal, placeholder_text="Prazo YYYY-MM-DD ou vazio")
        deadline_entry.pack(fill="x", padx=24, pady=12)

        def save():
            title = title_entry.get()
            description = description_entry.get()
            deadline_text = deadline_entry.get()

            deadline = date.fromisoformat(deadline_text) if deadline_text else None

            create_goal(title, description, deadline)

            modal.destroy()
            self.render_goals()

        save_button = ctk.CTkButton(modal, text="Salvar", command=save)
        save_button.pack(fill="x", padx=24, pady=24)

    def change_status(self, goal_id, status):
        update_goal_status(goal_id, status)
        self.render_goals()

    def remove_goal(self, goal_id):
        delete_goal(goal_id)
        self.render_goals()