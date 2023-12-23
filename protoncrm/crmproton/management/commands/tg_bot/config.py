from django.conf import settings
from environs import Env
from dataclasses import dataclass
from typing import List


@dataclass
class BotConfig:
    token: str
    admin_ids: List[int]
    use_redis: bool
    remind_time: int


def load_config():
    env: Env = Env()
    env.read_env(f'{settings.BASE_DIR}\\.env')
    token: str = env.str('TOKEN')
    admin_ids: List[int] = env.list('ADMIN_IDS')
    use_redis: bool = env.bool('USE_REDIS')
    remind_time: int = env.int('REMIND_TIME')
    return BotConfig(token=token, admin_ids=admin_ids, use_redis=use_redis,
                     remind_time=remind_time)
