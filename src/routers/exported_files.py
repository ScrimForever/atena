from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse
from starlette.status import HTTP_409_CONFLICT
from services.bucket import BucketService
from services.validate import ValidateJSON
from services.mergefiles import MergeFiles
from services.generate_report import GenerateReport
from loguru import logger

exported_files_router = APIRouter(tags=["EXPORTED FILES"], prefix="/exported")


@exported_files_router.post('/upload-files')
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    bucket_persist_files = await BucketService().files_persist(files)
    if bucket_persist_files:
        _is_valid = await ValidateJSON().validate_input_jsons()
        if _is_valid is True:
            await MergeFiles().merge()
            return await GenerateReport().generate()

        else:
            return _is_valid
    else:
        return JSONResponse(
            content={
                "message": "Some problem to upload files. Please, try again."
            },
            status_code=HTTP_409_CONFLICT
        )
