import os
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config import (
    GEMINI_API_KEY,
    GROQ_API_KEY
)

# =========================
# MODEL CONFIG
# =========================

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# =========================
# ERROR DETECTION
# =========================

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

# =========================
# MAIN LLM CLASS
# =========================

class ResearchLLM:

    def __init__(self):

        self.gemini = None
        self.groq = None

        # -----------------
        # Gemini
        # -----------------

        if GEMINI_API_KEY:

            self.gemini = ChatGoogleGenerativeAI(
                model=GEMINI_MODEL,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
            )

        # -----------------
        # Groq
        # -----------------

        if GROQ_API_KEY:

            self.groq = ChatGroq(
                model=GROQ_MODEL,
                api_key=GROQ_API_KEY,
                temperature=0.2,
            )

    # =========================
    # NORMAL INVOCATION
    # =========================

    def invoke(self, messages):

        # No Gemini → use Groq directly
        if self.gemini is None:

            if self.groq is None:
                raise RuntimeError(
                    "No LLM provider configured."
                )

            print("\nUSING GROQ\n")

            return self.groq.invoke(messages)

        # Try Gemini first
        try:

            print("\nUSING GEMINI\n")

            return self.gemini.invoke(messages)

        # Gemini failed
        except Exception as error:

            # Fallback to Groq
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

        # ---------------------------------
        # NO GEMINI → USE GROQ DIRECTLY
        # ---------------------------------

        if self.gemini is None:

            if self.groq is None:
                raise RuntimeError(
                    "No LLM provider configured."
                )

            print(
                "\nUSING GROQ STRUCTURED OUTPUT\n"
            )

            return self._groq_structured_call(
                schema,
                prompt
            )

        # ---------------------------------
        # TRY GEMINI STRUCTURED OUTPUT
        # ---------------------------------

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

        # ---------------------------------
        # GEMINI FAILED → SWITCH TO GROQ
        # ---------------------------------

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

                return self._groq_structured_call(
                    schema,
                    prompt
                )

            raise

    # =========================
    # GROQ STRUCTURED FALLBACK
    # =========================

    def _groq_structured_call(
        self,
        schema,
        prompt
    ):

        groq_prompt = f"""
Return ONLY valid JSON.

IMPORTANT:
- No markdown
- No explanations
- No comments
- No extra text

JSON SCHEMA:
{json.dumps(schema.model_json_schema(), indent=2)}

REQUEST:
{prompt}
"""

        response = self.groq.invoke(
            groq_prompt
        )

        content = response.content

        if not isinstance(content, str):
            content = str(content)

        # -------------------------
        # Extract JSON block
        # -------------------------

        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end == 0:

            raise ValueError(
                f"Groq did not return valid JSON.\n\n"
                f"Response:\n{content}"
            )

        json_text = content[start:end]

        # -------------------------
        # Parse JSON
        # -------------------------

        try:

            parsed = json.loads(
                json_text
            )

        except Exception as e:

            raise ValueError(
                f"Failed to parse Groq JSON.\n\n"
                f"JSON TEXT:\n{json_text}\n\n"
                f"ERROR:\n{e}"
            )

        # -------------------------
        # Validate with Pydantic
        # -------------------------

        try:

            return schema(**parsed)

        except Exception as e:

            raise ValueError(
                f"Schema validation failed.\n\n"
                f"PARSED JSON:\n{parsed}\n\n"
                f"ERROR:\n{e}"
            )

# =========================
# GLOBAL INSTANCE
# =========================

research_llm = ResearchLLM()