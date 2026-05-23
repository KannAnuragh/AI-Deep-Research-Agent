from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI:", GEMINI_API_KEY[:10] if GEMINI_API_KEY else "NOT FOUND")