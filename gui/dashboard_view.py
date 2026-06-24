import customtkinter as ctk

from repositories.habit_repository import list_habits
from repositories.goal_repository import list_goals
from services.habit_service import mark_habit
from repositories.goal_repository import update_goal_status


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F172A")
        self.build()

    def build(self):
        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 32, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Visão geral das suas metas e hábitos.",
            font=("Segoe UI", 15),
            text_color="#94A3B8"
        )
        subtitle.pack(anchor="w", pady=(4, 24))

        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x")

        habits = list_habits()
        goals = list_goals()

        active_habits = [h for h in habits if h[6]]
        active_goals = [g for g in goals if g[3] == "ativa"]

        best_streak = max([h[5] for h in habits], default=0)

        self.create_card("Hábitos ativos", str(len(active_habits)), 0)
        self.create_card("Metas ativas", str(len(active_goals)), 1)
        self.create_card("Melhor streak", f"{best_streak} dias", 2)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, pady=(28, 0))

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.habits_panel = ctk.CTkFrame(body, fg_color="#111827", corner_radius=18)
        self.habits_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        self.goals_panel = ctk.CTkFrame(body, fg_color="#111827", corner_radius=18)
        self.goals_panel.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

        self.render_habits_panel(active_habits)
        self.render_goals_panel(active_goals)

    def create_card(self, title, value, column):
        self.cards_frame.grid_columnconfigure(column, weight=1)

        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color="#111827",
            corner_radius=18,
            height=120
        )
        card.grid(row=0, column=column, sticky="ew", padx=8)
        card.pack_propagate(False)

        label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        label.pack(anchor="w", padx=20, pady=(18, 4))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 30, "bold"),
            text_color="#F8FAFC"
        )
        value_label.pack(anchor="w", padx=20)

    def render_habits_panel(self, habits):
        title = ctk.CTkLabel(
            self.habits_panel,
            text="Hábitos de hoje",
            font=("Segoe UI", 22, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w", padx=22, pady=(22, 16))

        for habit in habits:
            habit_id = habit[0]
            name = habit[1]
            streak = habit[4]

            row = ctk.CTkFrame(self.habits_panel, fg_color="#1E293B", corner_radius=14)
            row.pack(fill="x", padx=18, pady=8)

            label = ctk.CTkLabel(
                row,
                text=f"{name} — {streak} dias",
                font=("Segoe UI", 15),
                text_color="#F8FAFC"
            )
            label.pack(side="left", padx=16, pady=14)

            button = ctk.CTkButton(
                row,
                text="Concluir hoje",
                width=130,
                command=lambda hid=habit_id: self.complete_habit(hid)
            )
            button.pack(side="right", padx=12)

    def render_goals_panel(self, goals):
        title = ctk.CTkLabel(
            self.goals_panel,
            text="Metas ativas",
            font=("Segoe UI", 22, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w", padx=22, pady=(22, 16))

        for goal in goals:
            goal_id = goal[0]
            title_text = goal[1]

            row = ctk.CTkFrame(self.goals_panel, fg_color="#1E293B", corner_radius=14)
            row.pack(fill="x", padx=18, pady=8)

            label = ctk.CTkLabel(
                row,
                text=title_text,
                font=("Segoe UI", 15),
                text_color="#F8FAFC"
            )
            label.pack(side="left", padx=16, pady=14)

            button = ctk.CTkButton(
                row,
                text="Concluir",
                width=100,
                command=lambda gid=goal_id: self.complete_goal(gid)
            )
            button.pack(side="right", padx=12)

    def complete_habit(self, habit_id):
        mark_habit(habit_id, True)
        self.refresh()

    def complete_goal(self, goal_id):
        update_goal_status(goal_id, "concluida")
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build()