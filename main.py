import asyncio

from src.college_parser.routers.schedule import (
    app,
    root,
    get_schedule
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )