# ai/regex_patterns.py

INDIAN_PATTERNS = {
    "AADHAAR_ID": r"\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b|\b[2-9]{1}[0-9]{11}\b",
    "PAN_CARD": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
    "PHONE_NUMBER": r"\b(?:\+91|91)?[6-9][0-9]{9}\b",
    "PRIVATE_KEY": r"-----BEGIN\sRSA\sPRIVATE\sKEY-----|(?i)secret_key|(?i)api_key|(?i)passwd",
}

# Contextual keywords to increase confidence
CONTEXT_KEYWORDS = {
    "AADHAAR_ID": ["uidai", "aadhaar", "dob", "identity"],
    "PAN_CARD": ["income tax", "permanent account", "nsdl", "taxpayer"],
    "PHONE_NUMBER": ["mobile", "call", "whatsapp", "contact"]
}