from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from src.college_parser.routers import today_router, tomorrow_router
from src.college_parser.configs.groups import GROUPS

app = FastAPI(
    title="IT-COLLEGE Расписание",
    description="Сервис для получения расписания групп РПО-2 и РПО-3",
    version="1.0.0"
)

app.include_router(today_router)
app.include_router(tomorrow_router)

Instrumentator().instrument(app).expose(app, endpoint='/metrics')

@app.get("/", response_class=HTMLResponse)
async def root():
    """Красивая главная страница с выбором группы"""
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d.%m.%Y")

    options = "\n".join([
        f'<option value="{group}">{group}</option>' for group in GROUPS
    ])

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IT-COLLEGE | Расписание</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{ max-width: 1200px; padding: 20px; }}
            .hero {{ text-align: center; margin-bottom: 50px; }}
            .hero .badge {{
                display: inline-block;
                background: rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                padding: 8px 20px;
                border-radius: 50px;
                font-size: 0.85em;
                font-weight: 500;
                color: white;
                margin-bottom: 25px;
                border: 1px solid rgba(255,255,255,0.3);
            }}
            .hero h1 {{
                font-size: 3.5em;
                font-weight: 800;
                color: white;
                text-shadow: 0 2px 20px rgba(0,0,0,0.2);
            }}
            .hero .gradient-text {{
                background: linear-gradient(135deg, #fff, #f0f0f0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            .hero p {{
                font-size: 1.2em;
                color: rgba(255,255,255,0.95);
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.6;
            }}
            .stats {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-top: 30px;
                flex-wrap: wrap;
            }}
            .stat-card {{
                background: rgba(255,255,255,0.15);
                backdrop-filter: blur(10px);
                padding: 20px 30px;
                border-radius: 20px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.2);
                transition: transform 0.3s ease;
            }}
            .stat-card:hover {{ transform: translateY(-5px); background: rgba(255,255,255,0.25); }}
            .stat-number {{ font-size: 2.5em; font-weight: 800; color: white; display: block; }}
            .stat-label {{ font-size: 0.9em; color: rgba(255,255,255,0.9); margin-top: 5px; }}
            .group-selector {{
                background: rgba(255,255,255,0.15);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                margin-top: 30px;
                border: 1px solid rgba(255,255,255,0.2);
            }}
            .group-selector select {{
                padding: 12px 20px;
                border-radius: 12px;
                border: none;
                font-size: 1.1em;
                font-weight: 500;
                background: white;
                color: #1e293b;
                cursor: pointer;
                outline: none;
                min-width: 180px;
                margin-right: 12px;
            }}
            .group-selector .btn-group {{
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                justify-content: center;
                margin-top: 15px;
            }}
            .group-selector .btn {{
                padding: 12px 30px;
                border-radius: 12px;
                border: none;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                color: white;
                background: rgba(255,255,255,0.25);
            }}
            .group-selector .btn:hover {{
                transform: translateY(-3px);
                background: rgba(255,255,255,0.4);
            }}
            .group-selector .btn-today {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }}
            .group-selector .btn-tomorrow {{
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            }}
            .cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-top: 50px;
            }}
            .card {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                transition: all 0.3s ease;
                text-decoration: none;
                color: inherit;
                display: block;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }}
            .card-icon {{ font-size: 3em; margin-bottom: 15px; }}
            .card h3 {{ font-size: 1.5em; font-weight: 700; color: #1e293b; margin-bottom: 10px; }}
            .card p {{ color: #64748b; line-height: 1.5; font-size: 0.9em; }}
            .card .arrow {{
                margin-top: 15px;
                display: inline-block;
                color: #667eea;
                font-weight: 500;
            }}
            @media (max-width: 768px) {{
                .hero h1 {{ font-size: 2.2em; }}
                .stats {{ gap: 15px; }}
                .stat-card {{ padding: 15px 20px; }}
                .stat-number {{ font-size: 1.8em; }}
                .cards {{ grid-template-columns: 1fr; }}
                .group-selector select {{ width: 100%; margin-bottom: 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <div class="badge">🚀 Добро пожаловать</div>
                <h1><span class="gradient-text">IT-COLLEGE</span><br>Расписание группы</h1>
                <p>📱 Удобный сервис для просмотра расписания занятий<br>🔄 Данные обновляются ежедневно</p>
                <div class="stats">
                    <div class="stat-card"><span class="stat-number">📅</span><span class="stat-label">{current_date}</span></div>
                    <div class="stat-card"><span class="stat-number">🕐</span><span class="stat-label">{current_time}</span></div>
                </div>

                <div class="group-selector">
                    <form action="/schedule/today" method="get" id="todayForm">
                        <select name="group" id="groupSelect">
                            {options}
                        </select>
                    </form>
                    <div class="btn-group">
                        <button type="submit" form="todayForm" class="btn btn-today">📖 Расписание на сегодня</button>
                        <button type="submit" form="tomorrowForm" class="btn btn-tomorrow">📅 Расписание на завтра</button>
                    </div>
                    <form action="/schedule/tomorrow" method="get" id="tomorrowForm">
                        <input type="hidden" name="group" id="tomorrowGroupInput">
                    </form>
                </div>
            </div>

            <div class="cards">
                <a href="/docs" class="card">
                    <div class="card-icon">📚</div>
                    <h3>API Документация</h3>
                    <p>Swagger UI для разработчиков</p>
                    <span class="arrow">→ Открыть</span>
                </a>
            </div>
        </div>

        <script>
            const groupSelect = document.getElementById('groupSelect');
            const tomorrowInput = document.getElementById('tomorrowGroupInput');

            function syncTomorrowGroup() {{
                tomorrowInput.value = groupSelect.value;
            }}
            groupSelect.addEventListener('change', syncTomorrowGroup);
            syncTomorrowGroup();

            document.querySelector('form[action="/schedule/today"]').addEventListener('submit', function(e) {{
                console.log('Selected group for today:', groupSelect.value);
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)