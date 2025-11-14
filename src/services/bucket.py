from dataclasses import dataclass
from starlette.datastructures import UploadFile


@dataclass
class BucketService:

    async def files_persist(self, files: list[UploadFile]):

