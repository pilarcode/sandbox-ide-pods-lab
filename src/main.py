from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ide.api.routes import router as ide_router
from ide.utils import logger
from ide.utils.settings import settings
import os
# Create the FastAPI application instance
app = FastAPI(
    title="IDE API",
    description="API for managing the operations of the IDE.",    
)


@app.get("/health")
async def health_check():
    logger.get_logger(__name__).info("Health check endpoint called.")
    return {"status": "UP", "message": "Welcome to the Compi API!"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """ Custom exception handler for HTTP exceptions."""
    logger.get_logger(__name__).error(f"HTTP Exception: {exc.detail}",exc_info=True, stack_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Configure the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ide_router, prefix="")


if __name__ == "__main__":
    import uvicorn
    logger.init(level="DEBUG", save_log=True)
    logo = r"""
    ___ ____  _____ 
    |_ _|  _ \| ____|
    | || | | |  _|  
    | || |_| | |___ 
    |___|____/|_____|
    """

    logger.get_logger(__name__).info("\n" + logo)
    logger.get_logger(__name__).info("Starting the IDE API")
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)