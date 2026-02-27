import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def scan_reddit(username: str) -> dict:
    """
    Searches Reddit to see if the target username exists and gathers public footprint data.
    In OSINT, people often reuse the same username across GitHub, Reddit, and Pastebin.
    """
    if not username:
        return None

    # REDDIT TRICK: You MUST use a custom User-Agent, or they will block you instantly.
    # Format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
    headers = {
        "User-Agent": "python:tracepoint.osint.hackathon:v1.0 (by /u/TracePointApp)"
    }
    
    # We check the user's "about" page via their hidden JSON API
    url = f"https://www.reddit.com/user/{username}/about.json"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=5.0)
            
            if response.status_code == 200:
                data = response.json().get("data", {})
                
                # Check if the account is active or suspended
                is_suspended = data.get("is_suspended", False)
                created_utc = data.get("created_utc", "Unknown")
                link_karma = data.get("link_karma", 0)
                
                if is_suspended:
                    desc = f"Reddit account '{username}' found but is currently suspended."
                    risk = "LOW"
                else:
                    desc = f"Active Reddit profile found. Account has {link_karma} karma. High chance of cross-platform username reuse."
                    risk = "MEDIUM"

                return {
                    "platform": "Reddit",
                    "risk_level": risk,
                    "description": desc,
                    "pii_found": ["Username", "Activity Metadata"],
                    "url": f"https://www.reddit.com/user/{username}"
                }
                
            elif response.status_code == 404:
                # User does not exist, no footprint found here
                return None
                
            elif response.status_code == 429:
                logger.warning(f"⚠️ Reddit API Rate Limited for {username}")
                
    except Exception as e:
        logger.error(f"Reddit Scraper Error: {e}")

    # THE HACKATHON FAILSAFE
    # If the username is "demo" or Reddit blocks us during the pitch
    if username.lower() in ["demo", "admin", "test"]:
        logger.info("Injecting Fallback Demo Data for Reddit.")
        return {
            "platform": "Reddit (Simulated)",
            "risk_level": "MEDIUM",
            "description": "Profile found. User has posted in r/cybersecurity and r/hyderabad. Possible location leakage.",
            "pii_found": ["Username", "Geographic Location (Inferred)"],
            "url": f"https://www.reddit.com/user/{username}"
        }

    return None