

def get_post_headers() -> dict[str, str]:
    """Формирует заголовки, имитирующие браузер."""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru_RU, ru",
        "content-type": "application/json",
        "origin": "https://journal.top-academy.ru",
        "referer": "https://journal.top-academy.ru/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 YaBrowser/26.4.0.0 Safari/537.36",
    }
    return headers
