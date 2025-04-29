import re
from typing import Tuple

class Guardrails:
    # Simple regex patterns for PII (can be extended)
    EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}")
    PHONE_PATTERN = re.compile(r"\b\d{10,}\b")
    ADDRESS_KEYWORDS = ["street", "road", "avenue", "city", "zip", "postal", "country"]
    
    # Allow more math topics and keywords
    ALLOWED_TOPICS = [
        "math", "algebra", "geometry", "calculus", "trigonometry", "probability", "statistics",
        "number theory", "equation", "function", "integral", "derivative", "matrix", "vector",
        "education", "mathematics", "JEE", "exam", "problem", "solution", "proof",
        "area", "volume", "triangle", "circle", "sphere", "determinant", "sin", "cos", "tan",
        "solve", "find", "calculate", "compute", "value", "formula", "theorem"
    ]

    @staticmethod
    def contains_pii(text: str) -> bool:
        if Guardrails.EMAIL_PATTERN.search(text):
            return True
        if Guardrails.PHONE_PATTERN.search(text):
            return True
        for word in Guardrails.ADDRESS_KEYWORDS:
            if word in text.lower():
                return True
        return False

    @staticmethod
    def is_math_topic(text: str) -> bool:
        text_lower = text.lower()
        # Check for math symbols and operations
        math_symbols = ['+', '-', '*', '/', '=', '^', '√', 'π', 'sin', 'cos', 'tan', 'log', 'ln']
        if any(symbol in text_lower for symbol in math_symbols):
            return True
        # Check for math keywords
        return any(topic in text_lower for topic in Guardrails.ALLOWED_TOPICS)

    @classmethod
    def input_guardrail(cls, user_input: str) -> Tuple[bool, str]:
        if cls.contains_pii(user_input):
            return False, "Input rejected: contains personal or sensitive information."
        if not cls.is_math_topic(user_input):
            return False, "Input rejected: only mathematics or education-related questions are allowed."
        return True, ""

    @classmethod
    def output_guardrail(cls, response: str) -> Tuple[bool, str]:
        if cls.contains_pii(response):
            return False, "Output blocked: contains personal or sensitive information."
        if not cls.is_math_topic(response):
            return False, "Output blocked: only mathematics or education-related content is allowed."
        return True, "" 