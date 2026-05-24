import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config import GEMINI_API_KEY, GROQ_API_KEY


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def _is_gemini_quota_error(error):

    error_text = f"{type(error).__name__}: {error}".lower()

    return any(
        phrase in error_text
        for phrase in [
            "resource exhausted",
            "quota",
            "too many requests",
            "rate limit",
            "429",
        ]
    )


class ResearchLLM:

    def __init__(self):

        self.gemini = (
            ChatGoogleGenerativeAI(
                model=GEMINI_MODEL,
                api_key=GEMINI_API_KEY,
            )
            if GEMINI_API_KEY
            else None
        )

        self.groq = (
            ChatGroq(
                model=GROQ_MODEL,
                api_key=GROQ_API_KEY,
            )
            if GROQ_API_KEY
            else None
        )

    def invoke(self, messages):

        if self.gemini is None:

            if self.groq is None:
                raise RuntimeError("No Gemini or Groq API key is configured.")

            return self.groq.invoke(messages)

        try:
            return self.gemini.invoke(messages)
        except Exception as error:

            if self.groq is not None and _is_gemini_quota_error(error):
                print("Gemini quota exhausted, switching to Groq.")
                return self.groq.invoke(messages)

            raise


research_llm = ResearchLLM()