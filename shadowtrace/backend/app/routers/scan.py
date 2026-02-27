from fastapi import APIRouter, HTTPException
import asyncio
import logging

# Import our strict Pydantic models
from app.models.schemas import ScanRequest, ScanResponse

# Import our 4 OSINT Scrapers
from app.scrapers.github_scraper import scan_github
from app.scrapers.hibp import scan_hibp
from app.scrapers.reddit_scraper import scan_reddit
from app.scrapers.pastebin_scraper import scan_pastebin

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scan",
    tags=["Scanning Engine"]
)

def calculate_risk_score(exposures: list) -> int:
    """
    Hackathon Logic: Calculates a 0-100 risk score based on findings.
    """
    score = 0
    for exp in exposures:
        level = exp.get("risk_level", "LOW")
        if level == "CRITICAL":
            score += 40
        elif level == "HIGH":
            score += 30
        elif level == "MEDIUM":
            score += 15
        else:
            score += 5
            
    # Cap the maximum score at 100
    return min(score, 100)

@router.post("/", response_model=ScanResponse)
async def start_new_scan(request: ScanRequest):
    """
    Initiates a concurrent OSINT scan across GitHub, Reddit, Pastebin, and Known Breaches.
    """
    email = request.target_email
    username = request.target_username

    # OSINT Pivot: If no username is provided, guess it from the email (e.g., johndoe@gmail.com -> johndoe)
    if not username and "@" in email:
        username = email.split("@")[0]
        logger.info(f"No username provided. Pivoting to guessed username: '{username}'")

    logger.info(f"🔍 Starting concurrent OSINT scan for Email: {email} | Username: {username}")

    # 🚀 Run all 4 scrapers AT THE EXACT SAME TIME for massive speed
    tasks = [
        scan_github(email),
        scan_hibp(email),
        scan_pastebin(email),
        scan_reddit(username)
    ]
    
    # Wait for all scrapers to finish their jobs
    raw_results = await asyncio.gather(*tasks)
    
    # Filter out the 'None' results (where platforms found nothing or failed)
    exposures = [res for res in raw_results if res is not None]

    # Calculate the final risk score
    final_score = calculate_risk_score(exposures)

    # Construct the final response matching our schema exactly
    response_data = {
        "target": email,
        "total_leaks": len(exposures),
        "risk_score": final_score,
        "exposures": exposures
    }

    return response_data