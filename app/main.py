from fastapi import FastAPI, Depends, Request
import logging
import time
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.routes import upload, analyze
from app.utils.security import get_api_key
from app.utils.limiter import limiter

# Basic Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Veefy Backend Task")

# Rate Limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware for Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
    return response

# Include routers with global security dependency (Bonus)
# If you want public endpoints, move Depends to specific routes. 
# For this task, protecting everything is safer/simpler demo of "Auth".
app.include_router(upload.router, dependencies=[Depends(get_api_key)])
app.include_router(analyze.router, dependencies=[Depends(get_api_key)])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Veefy Backend Task API"}
