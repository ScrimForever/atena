from fastapi import FastAPI
from routers.exported_files import exported_files_router

app = FastAPI(
    description="Atena API",
    version="1.0a",
)

app.include_router(
    exported_files_router
)
