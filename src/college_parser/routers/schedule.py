from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime
from src.college_parser.utils.validation_get_response import get_schedule_today

app = FastAPI(
    title="IT-COLLEGE Расписание",
    description="Сервис для получения расписания группы РПО-3",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Красивый корневой эндпоинт"""
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d.%m.%Y")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IT-COLLEGE | Расписание</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                overflow-x: hidden;
            }}

            /* Анимированные круги на фоне */
            body::before {{
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                background: rgba(255,255,255,0.1);
                border-radius: 50%;
                top: -100px;
                right: -100px;
                animation: float 20s infinite;
            }}

            body::after {{
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: rgba(255,255,255,0.05);
                border-radius: 50%;
                bottom: -200px;
                left: -200px;
                animation: float 25s infinite reverse;
            }}

            @keyframes float {{
                0%, 100% {{ transform: translate(0, 0); }}
                50% {{ transform: translate(30px, 30px); }}
            }}

            .container {{
                position: relative;
                z-index: 1;
                width: 100%;
                max-width: 1200px;
                padding: 20px;
            }}

            .hero {{
                text-align: center;
                margin-bottom: 50px;
                animation: fadeInUp 0.8s ease;
            }}

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
                margin-bottom: 15px;
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

            .stat-card:hover {{
                transform: translateY(-5px);
                background: rgba(255,255,255,0.25);
            }}

            .stat-number {{
                font-size: 2.5em;
                font-weight: 800;
                color: white;
                display: block;
            }}

            .stat-label {{
                font-size: 0.9em;
                color: rgba(255,255,255,0.9);
                margin-top: 5px;
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
                cursor: pointer;
                text-decoration: none;
                color: inherit;
                display: block;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                animation: fadeInUp 0.8s ease backwards;
            }}

            .card:nth-child(1) {{ animation-delay: 0.1s; }}
            .card:nth-child(2) {{ animation-delay: 0.2s; }}
            .card:nth-child(3) {{ animation-delay: 0.3s; }}

            .card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            }}

            .card-icon {{
                font-size: 3em;
                margin-bottom: 15px;
            }}

            .card h3 {{
                font-size: 1.5em;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 10px;
            }}

            .card p {{
                color: #64748b;
                line-height: 1.5;
                font-size: 0.9em;
            }}

            .card .arrow {{
                margin-top: 15px;
                display: inline-block;
                color: #667eea;
                font-weight: 500;
            }}

            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @media (max-width: 768px) {{
                .hero h1 {{
                    font-size: 2.2em;
                }}
                .hero p {{
                    font-size: 1em;
                }}
                .stats {{
                    gap: 15px;
                }}
                .stat-card {{
                    padding: 15px 20px;
                }}
                .stat-number {{
                    font-size: 1.8em;
                }}
                .cards {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <div class="badge">
                    🚀 Добро пожаловать
                </div>
                <h1>
                    <span class="gradient-text">IT-COLLEGE</span><br>
                    Расписание группы РПО-3
                </h1>
                <p>
                    📱 Удобный сервис для просмотра расписания занятий<br>
                    🔄 Данные обновляются ежедневно
                </p>

                <div class="stats">
                    <div class="stat-card">
                        <span class="stat-number">📅</span>
                        <span class="stat-label">{current_date}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">🕐</span>
                        <span class="stat-label">{current_time}</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">👨‍🎓</span>
                        <span class="stat-label">РПО-3</span>
                    </div>
                </div>
            </div>

            <div class="cards">
                <a href="/schedule" class="card">
                    <div class="card-icon">📖</div>
                    <h3>Расписание на сегодня</h3>
                    <p>Актуальное расписание занятий группы РПО-3 с указанием времени, преподавателей и аудиторий</p>
                    <span class="arrow">→ Перейти к расписанию</span>
                </a>

                <a href="/docs" class="card">
                    <div class="card-icon">📚</div>
                    <h3>API Документация</h3>
                    <p>Swagger UI для разработчиков - интерактивная документация всех эндпоинтов API</p>
                    <span class="arrow">→ Открыть документацию</span>
                </a>

                <a href="/redoc" class="card">
                    <div class="card-icon">📄</div>
                    <h3>ReDoc</h3>
                    <p>Альтернативная документация API с удобной навигацией и поиском</p>
                    <span class="arrow">→ Открыть ReDoc</span>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content


@app.get("/schedule", response_class=HTMLResponse)
async def get_schedule():
    """Красивое отображение расписания"""
    schedule_text = await get_schedule_today()

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Расписание | IT-COLLEGE</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}

            .back-btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                padding: 10px 20px;
                border-radius: 50px;
                color: white;
                text-decoration: none;
                margin-bottom: 20px;
                transition: all 0.3s ease;
                border: 1px solid rgba(255,255,255,0.3);
            }}

            .back-btn:hover {{
                background: rgba(255,255,255,0.3);
                transform: translateX(-5px);
            }}

            .card {{
                background: white;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
                animation: fadeIn 0.5s ease;
            }}

            .header {{
                background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                color: white;
                padding: 35px 30px;
                text-align: center;
            }}

            .header h1 {{
                font-size: 2em;
                font-weight: 700;
                margin-bottom: 8px;
            }}

            .date {{
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(255,255,255,0.2);
                font-size: 0.9em;
            }}

            .schedule-content {{
                padding: 35px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                line-height: 1.7;
                background: #f8fafc;
                white-space: pre-wrap;
            }}

            .footer {{
                background: #f1f5f9;
                padding: 16px;
                text-align: center;
                font-size: 0.8em;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}

            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            @media (max-width: 600px) {{
                .schedule-content {{
                    padding: 20px;
                    font-size: 11px;
                }}
                .header h1 {{
                    font-size: 1.5em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← На главную</a>
            <div class="card">
                <div class="header">
                    <h1>🏫 Расписание занятий</h1>
                    <div>Группа РПО-3</div>
                    <div class="date">📅 {datetime.now().strftime("%d.%m.%Y")}</div>
                </div>
                <div class="schedule-content">
                    {schedule_text}
                </div>
                <div class="footer">
                    ⏰ Актуально на сегодня | 🔄 Обновляется ежедневно
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "schedule:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )