from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.college_parser.services.today_schedule_service import get_schedule_today

router = APIRouter(prefix="/schedule", tags=["Today Schedule"])

@router.get("/today", response_class=HTMLResponse)
async def get_today_schedule_view():
    """Красивое отображение расписания на сегодня"""
    try:
        schedule_text = await get_schedule_today()
        current_date = datetime.now().strftime("%d.%m.%Y")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Расписание на сегодня | IT-COLLEGE</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 40px 20px;
                }}
                .container {{ max-width: 900px; margin: 0 auto; }}
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
                .header h1 {{ font-size: 2em; font-weight: 700; margin-bottom: 8px; }}
                .header .date {{ font-size: 0.95em; opacity: 0.8; margin-top: 8px; }}
                .schedule-content {{
                    padding: 35px;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 14px;
                    line-height: 1.8;
                    background: #f8fafc;
                    white-space: pre-wrap;
                    min-height: 200px;
                }}
                .schedule-content .empty {{
                    color: #94a3b8;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.1em;
                    padding: 40px 0;
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
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                @media (max-width: 600px) {{
                    .schedule-content {{ padding: 20px; font-size: 11px; }}
                    .header h1 {{ font-size: 1.5em; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-btn">← На главную</a>
                <div class="card">
                    <div class="header">
                        <h1>🏫 Расписание на сегодня</h1>
                        <div class="date">📅 {current_date}</div>
                    </div>
                    <div class="schedule-content">{schedule_text if schedule_text else '<div class="empty">📭 Расписание на сегодня отсутствует</div>'}</div>
                    <div class="footer">⏰ Актуально на сегодня | 🔄 Обновляется ежедневно</div>
                </div>
            </div>
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении расписания: {str(error)}"
        ) from error
