from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import the routers we built
# Note: Ensure these files exist in your app/routers/ folder
try:
    from app.routers import scan
except ImportError:
    # This is a failsafe in case of pathing issues during development
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from app.routers import scan

# 1. Initialize the FastAPI App
app = FastAPI(
    title="TracePoint OSINT Engine",
    description="Backend API for real-time digital footprint scanning and PII detection",
    version="1.0.0"
)

# 2. Configure CORS (The Bridge to Frontend)
# This allows your React app (typically on port 3000) to talk to this API.
# We include multiple local variations to be 100% safe.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers (Content-Type, Authorization, etc.)
)

# 3. Include Routers
# This mounts your scanning logic under the /api/v1/scan prefix
app.include_router(scan.router, prefix="/api/v1")

# 4. Root Endpoint (Health Check)
@app.get("/", tags=["Health Check"])
async def root():
    """
    Basic endpoint to verify the server is running.
    """
    return {
        "status": "online",
        "message": "TracePoint API is live and accepting requests",
        "docs_url": "/docs"
    }

# Setup basic logging to see requests in the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 TracePoint Engine started successfully!")
