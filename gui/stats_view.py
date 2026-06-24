import customtkinter as ctk


class StatsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F172A")
        self.build()

    def build(self):
        title = ctk.CTkLabel(
            self,
            text="Estatísticas",
            font=("Segoe UI", 32, "bold"),
            text_color="#F8FAFC"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            self,
            text="Aqui futuramente vamos colocar gráficos semanais, taxa de conclusão, ranking de hábitos e evolução das metas.",
            font=("Segoe UI", 15),
            text_color="#94A3B8",
            wraplength=800,
            justify="left"
        )
        subtitle.pack(anchor="w", pady=(8, 24))

        card = ctk.CTkFrame(self, fg_color="#111827", corner_radius=18)
        card.pack(fill="both", expand=True)

        label = ctk.CTkLabel(
            card,
            text="📊 Área reservada para gráficos e resumos",
            font=("Segoe UI", 22, "bold"),
            text_color="#F8FAFC"
        )
        label.pack(expand=True)