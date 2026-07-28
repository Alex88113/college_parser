from dataclasses import dataclass

@dataclass
class RedisSettings:
    decode_responses: bool = True
    max_connections: int = 20
    ttl: int = 3600
    socket_timeout: int = 10
    socket_connect_timeout: int = 15


redis_settings = RedisSettings()
