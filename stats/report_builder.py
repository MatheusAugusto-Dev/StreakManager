from datetime import date
from stats.stats_service import get_weekly_stats


def build_weekly_report_html():
    data = get_weekly_stats()

    start = data["start"].strftime("%d/%m/%Y")
    end = data["end"].strftime("%d/%m/%Y")

    rows_html = ""

    for goal in data["goals"]:
        unit = {
            "time": "min",
            "pages": "páginas",
            "chapters": "capítulos"
        }.get(goal["metric_type"], "")

        status = "✅ OK"
        if goal["expected"] is not None and goal["count"] < goal["expected"]:
            status = "⚠️ Atenção"

        rows_html += f"""
        <div class="goal">
            <h3>{goal["title"]}</h3>
            <p>Total: <strong>{goal['total']} {unit}</strong></p>
            <p>Check-ins: {goal["count"]}</p>
            <p>Status: {status}</p>
        </div>
        """

    return f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Relatório Semanal</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                    padding: 24px;
                }}
                .container {{
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 24px;
                    border-radius: 8px;
                }}
                .goal {{
                    border-top: 1px solid #eee;
                    padding-top: 12px;
                    margin-top: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Relatório Semanal</h1>
                <p>Período: <strong>{start}</strong> até <strong>{end}</strong></p>

                {rows_html}
            </div>
        </body>
        </html>"""
