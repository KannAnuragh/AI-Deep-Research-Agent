import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config import (
    GEMINI_API_KEY,
    GROQ_API_KEY
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

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

        self.gemini = None
        self.groq = None

        if GEMINI_API_KEY:

            self.gemini = ChatGoogleGenerativeAI(
                model=GEMINI_MODEL,
                google_api_key=GEMINI_API_KEY,
            )

        if GROQ_API_KEY:

            self.groq = ChatGroq(
                model=GROQ_MODEL,
                api_key=GROQ_API_KEY,
            )

    # =========================
    # NORMAL INVOCATION
    # =========================

    def invoke(self, messages):

        if self.gemini is None:

            if self.groq is None:
                raise RuntimeError(
                    "No LLM provider configured."
                )

            print("\nUSING GROQ\n")

            return self.groq.invoke(messages)

        try:

            print("\nUSING GEMINI\n")

            return self.gemini.invoke(messages)

        except Exception as error:

            if (
                self.groq
                and _is_gemini_quota_error(error)
            ):

                print(
                    "\nGEMINI QUOTA EXHAUSTED\n"
                    "SWITCHING TO GROQ\n"
                )

                return self.groq.invoke(messages)

            raise

    # =========================
    # STRUCTURED OUTPUTS
    # =========================

    def invoke_structured(
        self,
        schema,
        prompt
    ):

        if self.gemini is None:

            if self.groq is None:
                raise RuntimeError(
                    "No LLM provider configured."
                )

            print(
                "\nUSING GROQ STRUCTURED OUTPUT\n"
            )

            groq_structured = (
                self.groq.with_structured_output(
                    schema
                )
            )

            return groq_structured.invoke(prompt)

        try:

            print(
                "\nUSING GEMINI STRUCTURED OUTPUT\n"
            )

            gemini_structured = (
                self.gemini.with_structured_output(
                    schema
                )
            )

            return gemini_structured.invoke(prompt)

        except Exception as error:

            if (
                self.groq
                and _is_gemini_quota_error(error)
            ):

                print(
                    "\nGEMINI STRUCTURED OUTPUT "
                    "QUOTA EXHAUSTED\n"
                    "SWITCHING TO GROQ\n"
                )

                groq_structured = (
                    self.groq.with_structured_output(
                        schema
                    )
                )

                return groq_structured.invoke(prompt)

            raise

research_llm = ResearchLLM()