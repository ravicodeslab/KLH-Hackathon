# ai/pii_categories.py

PII_CONFIG = {
    "AADHAAR_ID": {
        "risk": "HIGH", 
        "category": "Government ID",
        "legal_impact": "Violation of DPDP Act Sec 4 (Personal Data Breach)",
        "remediation": "Rotate linked bank accounts and lock Aadhaar via UIDAI portal."
    },
    "PAN_CARD": {
        "risk": "CRITICAL", 
        "category": "Financial Identifier",
        "legal_impact": "Financial Data Exposure under DPDP Rules",
        "remediation": "Monitor CIBIL report for unauthorized loan applications."
    },
    "PRIVATE_KEY": {
        "risk": "CRITICAL", 
        "category": "Security Credential",
        "legal_impact": "Systemic Security Risk",
        "remediation": "Immediate revocation of the key and audit of access logs."
    },
    "PHONE_NUMBER": {
        "risk": "MEDIUM", 
        "category": "Contact Information",
        "legal_impact": "Privacy Invasion / Marketing Harassment",
        "remediation": "Enable DND and monitor for SIM-swap attempts."
    }
}