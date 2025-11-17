import os.path
from dataclasses import dataclass
from starlette.datastructures import UploadFile
import aiofiles
from loguru import logger
from utils.settings_config import settings



BUFFER_SIZE = 1024 * 1024


@dataclass
class BucketService:

    @staticmethod
    async def files_persist(files: list[UploadFile]):
        try:
            for file in files:
                file_path_uploaded = os.path.join(settings.upload_files_bucket, file.filename)
                async with aiofiles.open(file_path_uploaded, "wb") as f:
                    while content := await file.read(BUFFER_SIZE):
                        await f.write(content)
            return True
        except Exception as e:
            logger.error(e)
            return False
