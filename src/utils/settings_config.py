from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):


    upload_files_bucket: str = "bucket_folder"

    model_config = SettingsConfigDict()
    

settings = Settings()
