import customtkinter as ctk

from gui.dashboard_view import DashboardView
from gui.habits_view import HabitsView
from gui.goals_view import GoalsView
from gui.stats_view import StatsView


class StreakManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Streak Manager")
        self.geometry("1200x720")
        self.minsize(1000, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#0F172A")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#111827"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.content = ctk.CTkFrame(
            self,
            fg_color="#0F172A",
            corner_radius=0
        )
        self.content.grid(row=0, column=1, sticky="nsew")

        self.create_sidebar()

        self.current_view = None
        self.show_dashboard()

    def create_sidebar(self):
        title = ctk.CTkLabel(
            self.sidebar,
            text="Streak\nManager",
            font=("Segoe UI", 26, "bold"),
            text_color="#F8FAFC",
            justify="left"
        )
        title.pack(pady=(32, 24), padx=24, anchor="w")

        self.add_nav_button("Dashboard", self.show_dashboard)
        self.add_nav_button("Hábitos", self.show_habits)
        self.add_nav_button("Metas", self.show_goals)
        self.add_nav_button("Estatísticas", self.show_stats)

    def add_nav_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            height=44,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#1E293B",
            anchor="w",
            font=("Segoe UI", 15)
        )
        button.pack(fill="x", padx=16, pady=6)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def change_view(self, view_class):
        self.clear_content()
        self.current_view = view_class(self.content)
        self.current_view.pack(fill="both", expand=True, padx=28, pady=28)

    def show_dashboard(self):
        self.change_view(DashboardView)

    def show_habits(self):
        self.change_view(HabitsView)

    def show_goals(self):
        self.change_view(GoalsView)

    def show_stats(self):
        self.change_view(StatsView)