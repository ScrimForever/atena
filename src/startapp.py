from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.exported_files import exported_files_router

app = FastAPI(
    description="Atena API",
    version="1.0a",
)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    exported_files_router
)
