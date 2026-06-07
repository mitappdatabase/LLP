"""
Innovate Enterprise LLP - FastAPI Backend
Production-grade API server
"""

from .core.config import settings
from .core.security import create_access_token, verify_password, get_password_hash

__version__ = "1.0.0"
__author__ = "Innovate Enterprise LLP"
