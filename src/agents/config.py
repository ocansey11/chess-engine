import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")