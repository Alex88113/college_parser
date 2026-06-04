# utils/logger.py
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Создаём папку для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Убираем стандартный вывод (чтобы настроить с нуля)
logger.remove()

# ========== 1. КОНСОЛЬ (цветной вывод) ==========
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
    backtrace=True,
    diagnose=True,
)

# ========== 2. ФАЙЛ: все логи (DEBUG и выше) ==========
logger.add(
    LOG_DIR / "app_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
    level="DEBUG",
    rotation="1 day",  # новый файл каждый день
    retention="30 days",  # хранить 30 дней
    compression="zip",  # сжимать старые логи
    encoding="utf-8",
)

# ========== 3. ФАЙЛ: только ошибки (ERROR и выше) ==========
logger.add(
    LOG_DIR / "errors_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
    level="ERROR",
    rotation="1 day",
    retention="90 days",
    compression="zip",
    encoding="utf-8",
    backtrace=True,  # показывает стек вызовов
    diagnose=True,  # показывает значения переменных
)

# ========== 4. ФАЙЛ: JSON (для машинного чтения, опционально) ==========
logger.add(
    LOG_DIR / "app.json",
    serialize=True,  # JSON формат
    level="INFO",
    rotation="10 MB",
    retention="14 days",
)

