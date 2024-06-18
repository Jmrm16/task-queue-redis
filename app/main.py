from fastapi import FastAPI
from app.config import settings
from app.api.tasks import router as tasks_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


app.include_router(tasks_router, prefix=settings.API_V1_STR)
