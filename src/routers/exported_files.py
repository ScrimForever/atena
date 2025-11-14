from fastapi import APIRouter, UploadFile, File


exported_files_router = APIRouter(tags=["EXPORTED FILES"], prefix="/exported")


@exported_files_router.post('/upload-files')
async def upload_multiple_files(files: list[UploadFile] = File(...)):

    """
    upload_files_paths = []
    for file in files:
        file_path = os.path.join(BUCKET_FILES, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                while contents := await file.read(1024 * 1024):
                    buffer.write(contents)
            upload_files_paths.append(file_path)
        except Exception as e:
            return JSONResponse(
                content={
                    "message": f"There was an error: {file.filename} - Error: {e}"
                },
                status_code=HTTP_409_CONFLICT
            )
        finally:
            await file.close()

    return JSONResponse(
        content={
            "message": f"Successfully uploaded files"
        },
        status_code=HTTP_200_OK
    )
    """