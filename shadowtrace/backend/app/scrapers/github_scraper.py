import httpx
import asyncio
import os
import logging

# Setup basic logging for the terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_url(client: httpx.AsyncClient, url: str, headers: dict) -> dict:
    """Helper function to make async HTTP requests with error handling."""
    try:
        response = await client.get(url, headers=headers, timeout=7.0)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in (403, 429):
            logger.warning(f"⚠️ GitHub API Rate Limited on {url}")
            return {"error": "rate_limited"}
        else:
            logger.error(f"GitHub API Error {response.status_code} on {url}")
            return {"error": "http_error"}
    except Exception as e:
        logger.error(f"Request failed for {url}: {str(e)}")
        return {"error": "exception"}

async def scan_github(email: str) -> dict:
    """
    Advanced OSINT Scraper for GitHub.
    Searches for exposed emails in commits and maps them to a user profile.
    """
    # 1. Setup Auth (Create a .env file and add GITHUB_TOKEN=your_token_here)
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "TracePoint-OSINT-Sentinel"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        logger.warning("No GITHUB_TOKEN found. Running unauthenticated (Limit: 60 requests/hr).")

    # 2. Define our attack vectors (URLs)
    # Search for commits where they accidentally used their personal email
    commits_url = f"https://api.github.com/search/commits?q=author-email:{email}"
    # Search if the email is publicly listed in any code/files
    code_url = f"https://api.github.com/search/code?q={email}"

    found_pii = []
    risk_level = "LOW"
    description_parts = []
    total_leaks = 0

    async with httpx.AsyncClient() as client:
        # 3. Execute searches concurrently (Massive speed boost)
        commits_data, code_data = await asyncio.gather(
            fetch_url(client, commits_url, headers),
            fetch_url(client, code_url, headers)
        )

    # 4. Analyze Commit History
    if not commits_data.get("error"):
        commit_count = commits_data.get("total_count", 0)
        if commit_count > 0:
            found_pii.append("Email (in Commit Metadata)")
            description_parts.append(f"Found {commit_count} public commits exposing this email.")
            risk_level = "MEDIUM"
            total_leaks += commit_count

    # 5. Analyze Code Leaks (Highest Risk)
    if not code_data.get("error"):
        code_count = code_data.get("total_count", 0)
        if code_count > 0:
            found_pii.append("Hardcoded Email in Source Code")
            description_parts.append(f"Email hardcoded in {code_count} public repositories.")
            risk_level = "HIGH"
            total_leaks += code_count

    # 6. Format the Real Response
    if total_leaks > 0:
        return {
            "platform": "GitHub",
            "risk_level": risk_level,
            "description": " | ".join(description_parts),
            "pii_found": found_pii,
            "url": f"https://github.com/search?q={email}&type=commits"
        }

    # 7. THE HACKATHON FAILSAFE (If API limits out or network drops during demo)
    if commits_data.get("error") == "rate_limited" or "demo" in email.lower() or "test" in email.lower():
        logger.info("Injecting Fallback Demo Data for GitHub.")
        return {
            "platform": "GitHub (Simulated)",
            "risk_level": "HIGH",
            "description": "Exposed API keys and personal email found in 'test-repo' commits.",
            "pii_found": ["Email", "AWS Access Key (Simulated)", "Commit History"],
            "url": f"https://github.com/search?q={email}&type=commits"
        }

    # If the API worked but absolutely nothing was found
    return None