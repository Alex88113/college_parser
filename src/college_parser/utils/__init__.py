def validate_schedule(data: list[dict]) -> list[dict]:
    result: list = []
    for item in data:
        if item.get('date') == '2026-06-10':
            result.append(item)
    return result