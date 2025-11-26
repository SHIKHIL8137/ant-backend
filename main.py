from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
from contextlib import asynccontextmanager

from routers.resume import router as resume_router
from routers.session import router as session_router
from core.error_handler import register_exception_handlers
from core.logger import logger

load_dotenv()
PORT = int(os.getenv("PORT", 8000))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---------------- STARTUP ----------------
    logger.info("Starting Athena Backend...")
    logger.info("Initializing services...")
    # await redis.connect()  # example
    logger.info("Athena backend started successfully")

    yield  # FastAPI runs the application here

    # ---------------- SHUTDOWN ----------------
    logger.info("Shutting down Athena Backend...")
    # await redis.disconnect()  # example
    logger.info("Cleaning up resources...")
    logger.info("Server stopped gracefully")


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.include_router(resume_router, prefix="/resume")
app.include_router(session_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "Server running"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )