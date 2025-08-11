"""
Configuration file for ADGM Corporate Agent
Contains all settings, requirements, and rules
"""

import os

# Ollama Configuration
OLLAMA_MODEL = "llama2"  # Can use "mistral", "phi", "codellama", etc.
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 30  # seconds

# Embedding Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
CHROMA_COLLECTION_NAMES = [
    "adgm_regulations",
    "document_templates",
    "compliance_rules",
    "legal_precedents"
]

# ADGM Document Requirements
ADGM_REQUIREMENTS = {
    "company_incorporation": {
        "required_documents": [
            "Articles of Association",
            "Board Resolution",
            "Shareholder Resolution",
            "Incorporation Application Form",
            "Register of Members and Directors"
        ],
        "optional_documents": [
            "UBO Declaration Form",
            "Memorandum of Association",
            "Power of Attorney",
            "Passport Copies",
            "Proof of Address"
        ]
    },
    "licensing": {
        "required_documents": [
            "License Application Form",
            "Business Plan",
            "Compliance Manual",
            "Board Resolution for License",
            "Financial Projections"
        ],
        "optional_documents": [
            "Reference Letters",
            "CV of Key Personnel",
            "Organization Chart"
        ]
    },
    "employment": {
        "required_documents": [
            "Employment Contract",
            "Job Description",
            "Salary Certificate"
        ],
        "optional_documents": [
            "Offer Letter",
            "Non-Disclosure Agreement",
            "Non-Compete Agreement"
        ]
    },
    "commercial_agreement": {
        "required_documents": [
            "Commercial Agreement",
            "Terms and Conditions"
        ],
        "optional_documents": [
            "Schedule of Services",
            "Pricing Annex",
            "Service Level Agreement"
        ]
    }
}

# ADGM Rules and Regulations
ADGM_RULES = {
    "jurisdiction": "Abu Dhabi Global Market",
    "governing_law": "ADGM Laws and Regulations",
    "courts": "ADGM Courts",
    "arbitration": "ADGM Arbitration Centre",
    "regulations": {
        "companies": "ADGM Companies Regulations 2020",
        "employment": "ADGM Employment Regulations 2019",
        "data_protection": "ADGM Data Protection Regulations 2021",
        "financial_services": "ADGM Financial Services and Markets Regulations 2015",
        "insolvency": "ADGM Insolvency Regulations 2016"
    },
    "requirements": {
        "minimum_directors": 1,
        "minimum_shareholders": 1,
        "minimum_share_capital": "No minimum requirement",
        "registered_office": "Must be in ADGM",
        "company_secretary": "Optional for private companies",
        "annual_return": "Required annually",
        "audit": "Required for certain companies"
    }
}

# Red Flag Patterns
RED_FLAGS = {
    "jurisdiction": [
        "UAE Federal Courts",
        "Dubai Courts",
        "Abu Dhabi Courts",
        "Sharjah Courts",
        "DIFC",
        "Dubai International Financial Centre",
        "mainland UAE",
        "onshore UAE"
    ],
    "missing_elements": [
        "signatory section",
        "date field",
        "company name",
        "share capital",
        "registered office",
        "directors",
        "shareholders"
    ],
    "weak_language": [
        "may",
        "might",
        "could",
        "possibly",
        "perhaps",
        "should consider",
        "maybe",
        "potentially",
        "presumably",
        "arguably"
    ],
    "incorrect_terms": [
        "LLC" # When it should be "Ltd" for ADGM
        "Incorporated" # When it should be "Limited"
        "Corp" # Not standard for ADGM
    ]
}

# Document Templates Structure
DOCUMENT_TEMPLATES = {
    "articles_of_association": {
        "required_sections": [
            "Company Name and Suffix",
            "Registered Office",
            "Objects and Powers",
            "Share Capital",
            "Share Classes",
            "Directors",
            "Shareholders",
            "Meetings",
            "Dividends",
            "Accounts and Audit",
            "Winding Up",
            "Governing Law",
            "Jurisdiction"
        ],
        "standard_clauses": {
            "jurisdiction": "This Company shall be governed by the laws of Abu Dhabi Global Market.",
            "disputes": "Any disputes shall be resolved by the ADGM Courts.",
            "registered_office": "The registered office of the Company shall be situated in Abu Dhabi Global Market."
        }
    },
    "board_resolution": {
        "required_sections": [
            "Company Name",
            "Date and Time",
            "Venue",
            "Directors Present",
            "Quorum",
            "Resolutions",
            "Signatures"
        ],
        "standard_language": [
            "IT WAS RESOLVED",
            "BE IT RESOLVED",
            "RESOLVED THAT",
            "FURTHER RESOLVED"
        ]
    },
    "shareholder_resolution": {
        "required_sections": [
            "Company Name",
            "Date",
            "Shareholders",
            "Shareholdings",
            "Resolutions",
            "Signatures"
        ],
        "standard_language": [
            "WE, THE UNDERSIGNED",
            "IT WAS RESOLVED",
            "RESOLVED UNANIMOUSLY"
        ]
    }
}

# Compliance Scoring Weights
COMPLIANCE_WEIGHTS = {
    "critical": 10,
    "high": 5,
    "medium": 2,
    "low": 1,
    "info": 0
}

# Processing Settings
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB
SUPPORTED_FORMATS = [".docx"]
OUTPUT_DIRECTORY = "output"
TEMP_DIRECTORY = "temp"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "adgm_agent.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# RAG Settings
RAG_CHUNK_SIZE = 500
RAG_CHUNK_OVERLAP = 50
RAG_TOP_K_RETRIEVAL = 10
RAG_RERANK_TOP_K = 5
RAG_CONFIDENCE_THRESHOLD = 0.7

# Cache Settings
ENABLE_CACHING = True
CACHE_TTL = 3600  # 1 hour in seconds
MAX_CACHE_SIZE = 100  # Maximum number of cached queries

# API Rate Limiting (if needed in future)
RATE_LIMIT_ENABLED = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 60  # seconds

# Export Settings
EXPORT_FORMATS = ["docx", "pdf", "json"]
INCLUDE_METADATA = True
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Notification Messages
MESSAGES = {
    "welcome": "Welcome to ADGM Corporate Agent - Your AI-powered legal document review system",
    "processing": "Processing your documents...",
    "complete": "Document review complete!",
    "error": "An error occurred during processing. Please try again.",
    "missing_docs": "Missing required documents detected.",
    "all_docs_present": "All required documents uploaded.",
    "high_severity": "High-severity issues detected. Please review before submission.",
    "pass": "Documents appear compliant with ADGM regulations.",
    "fail": "Documents require corrections before submission."
}

# ADGM Specific Terms Dictionary
ADGM_TERMS = {
    "ADGM": "Abu Dhabi Global Market",
    "FSRA": "Financial Services Regulatory Authority",
    "RA": "Registration Authority",
    "AoA": "Articles of Association",
    "MoA": "Memorandum of Association",
    "UBO": "Ultimate Beneficial Owner",
    "KYC": "Know Your Customer",
    "AML": "Anti-Money Laundering",
    "CFT": "Combating Financing of Terrorism"
}

# Validation Rules
VALIDATION_RULES = {
    "company_name": {
        "min_length": 3,
        "max_length": 100,
        "required_suffix": ["Limited", "Ltd", "LLC", "Inc"],
        "prohibited_words": ["Bank", "Insurance", "Trust", "Royal", "Government"]
    },
    "share_capital": {
        "currencies": ["USD", "AED", "GBP", "EUR"],
        "min_value": 0,
        "max_value": None
    },
    "directors": {
        "minimum": 1,
        "maximum": None,
        "age_requirement": 18
    },
    "shareholders": {
        "minimum": 1,
        "maximum": 50  # For private companies
    }
}

# Default Values
DEFAULTS = {
    "currency": "USD",
    "financial_year_end": "December 31",
    "quorum": "majority",
    "notice_period": "14 days",
    "voting_threshold": "simple majority"
}