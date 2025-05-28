from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBotConfig:
    token: str

@dataclass
class DatabaseConfig:
    localdb: str  # Локальная база sqlite
    testdb: str = ""  # Тестовая база sqlite

    def get_local_url(self)->str:
        return f"sqlite:///{self.localdb}"
    def get_test_url(self)->str:
        return f"sqlite:///{self.testdb}"

@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db: DatabaseConfig
    path_img:str

def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TelegramBotConfig(token=env.str('BOT_TOKEN')),
        db=DatabaseConfig(
            localdb=env.str('LOCAL_DB_PATH'),
        ),
        path_img=env.str('PATH_IMG')
    )
