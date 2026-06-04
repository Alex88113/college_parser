from src.journal_project.utils.validation_post_response import get_valid_token

async def get_token() -> str:
    token = await get_valid_token()
    return token

async def get_headers() -> dict:
    token = await get_token()
    """Возвращает заголовки, имитирующие запрос из браузера."""
    return {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru_RU, ru",
        "authorization": f"Bearer {token}",
        "origin": "https://journal.top-academy.ru",
        "referer": "https://journal.top-academy.ru/",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "YaBrowser";v="26.4", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 YaBrowser/26.4.0.0 Safari/537.36"
    }