from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    DB_USER: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    PROVIDER_TOKEN: str
    BOT_TOKEN: str

    @property
    def dsn(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def create_invoice_url(self):
        return f"https://api.telegram.org/bot{self.BOT_TOKEN}/createInvoiceLink"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
