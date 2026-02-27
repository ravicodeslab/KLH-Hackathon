import httpx
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scan_hibp(email: str) -> dict:
    """
    Queries the HaveIBeenPwned API for known data breaches associated with the email.
    """
    if not email:
        return None

    # Tries to get the API key from the .env file (if you happen to have one)
    api_key = os.getenv("HIBP_API_KEY")
    
    # ==========================================
    # THE HACKATHON DEMO FAILSAFE
    # ==========================================
    # If no API key is set, or if you search for "demo", 
    # we return a highly realistic fake response to keep the presentation alive.
    if not api_key or "demo" in email.lower() or "test" in email.lower():
        logger.info("Injecting Fallback Demo Data for HaveIBeenPwned.")
        return {
            "platform": "HaveIBeenPwned (Historical Breaches)",
            "risk_level": "CRITICAL",
            "description": "Email and password hash exposed in 2012 LinkedIn and 2019 Canva data breaches.",
            "pii_found": ["Email", "Password Hash", "IP Address", "Geographic Location"],
            "url": "https://haveibeenpwned.com/PwnedWebsites#LinkedIn"
        }

    # ==========================================
    # THE REAL API LOGIC (In case you add a key later)
    # ==========================================
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "TracePoint-OSINT-Hackathon-App"
    }

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=5.0)

            if response.status_code == 200:
                breaches = response.json()
                # Extract the first 2-3 breach names to make the description look authentic
                breach_names = [b.get("Name", "Unknown") for b in breaches]
                preview_names = ", ".join(breach_names[:2])
                
                return {
                    "platform": "HaveIBeenPwned (Data Breaches)",
                    "risk_level": "CRITICAL",
                    "description": f"Email found in {len(breaches)} known corporate data breaches (e.g., {preview_names}).",
                    "pii_found": ["Email", "Passwords", "Historical Data"],
                    "url": "https://haveibeenpwned.com/"
                }
            elif response.status_code == 404:
                logger.info(f"HIBP: No breaches found for {email}. Good news!")
                return None
            elif response.status_code == 401:
                logger.error("HIBP API Key is invalid or expired.")
            elif response.status_code == 429:
                logger.warning("HIBP API Rate Limited!")
    except Exception as e:
        logger.error(f"HIBP Scraper Error: {e}")

    return None