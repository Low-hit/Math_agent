from guardrails import Guardrails
from feedback import FeedbackCollector
from typing import Dict, Optional
import sympy as sp
from knowledge_base import KnowledgeBase
import wolframalpha

class Router:
    def __init__(self, kb, websearch):
        self.kb = kb
        self.websearch = websearch
        self.guardrails = Guardrails()
        self.feedback_collector = FeedbackCollector()

    def route(self, user_input: str) -> Dict:
        """Route the user input to appropriate handler and collect feedback."""
        # First try knowledge base
        
        kb_result = self.kb.query(user_input)
        if kb_result:
            # Collect feedback on knowledge base result
            feedback = self.feedback_collector.collect_feedback(
                user_input, kb_result, {'accuracy': 0, 'clarity': 0, 'relevance': 0, 'comments': ''}
            )
            return {
                **kb_result,
                "feedback": feedback,
                "source": "Knowledge Base"
            }
        
        # If no result from knowledge base, try web search
        if self.websearch:
            web_result = self.websearch.search_math_content(user_input)
            if web_result:
                # Collect feedback on web search result
                feedback = self.feedback_collector.collect_feedback(
                    user_input, web_result, {'accuracy': 0, 'clarity': 0, 'relevance': 0, 'comments': ''}
                )
                return {
                    **web_result,
                    "feedback": feedback,
                    "source": "Web Search"
                }
        
        # Symbolic fallback for derivatives and equation solving
        x = sp.symbols('x')
        if "derivative" in user_input and "of" in user_input:
            expr = user_input.split("of")[-1].strip()
            try:
                derivative = sp.diff(sp.sympify(expr), x)
                return {
                    "answer": f"The derivative of {expr} is {derivative}.",
                    "steps": ["Parsed the expression.", "Used SymPy to compute the derivative."],
                    "source": "Symbolic Math"
                }
            except Exception as e:
                pass
        if "solve" in user_input and "=" in user_input:
            try:
                eq = user_input.split("solve")[-1].strip()
                solution = sp.solve(sp.sympify(eq))
                return {
                    "answer": f"The solution(s) to {eq} is/are {solution}.",
                    "steps": ["Parsed the equation.", "Used SymPy to solve the equation."],
                    "source": "Symbolic Math"
                }
            except Exception as e:
                pass
        # Symbolic fallback for area of a square
        if "area" in user_input and "square" in user_input and "side" in user_input:
            import re
            match = re.search(r"side\s*(\d+)", user_input)
            if match:
                side = int(match.group(1))
                area = side * side
                return {
                    "answer": f"The area of a square with side {side} is {area} square units.",
                    "steps": [
                        "Recall the formula for the area of a square: A = side².",
                        f"Substitute side = {side}: A = {side}² = {area}."
                    ],
                    "source": "Symbolic Math"
                }
        
        # If no results found
        return {
            "answer": "I'm sorry, I couldn't find an answer to your question.",
            "steps": ["No relevant information found in knowledge base or web search."],
            "source": "No Source",
            "feedback": self.feedback_collector.collect_feedback(
                user_input, {}, {'accuracy': 0, 'clarity': 0, 'relevance': 0, 'comments': ''}
            )
        }

    def get_feedback_summary(self) -> Dict:
        """
        Get a summary of all feedback collected.
        """
        return self.feedback_collector.get_feedback_summary()

x = sp.symbols('x')
result = sp.diff(sp.log(x), x)
# result will be 1/x

kb = KnowledgeBase()
kb.add_entry(
    "What is the derivative of log x?",
    "The derivative of log(x) is 1/x.",
    [
        "Recall the derivative rule for logarithmic functions.",
        "The derivative of log(x) with respect to x is 1/x."
    ]
)

class WebSearch:
    def __init__(self, app_id):
        self.client = wolframalpha.Client(app_id)

    def search_math_content(self, query: str):
        try:
            res = self.client.query(query)
            answer = next(res.results).text
            return {
                'success': True,
                'answer': answer,
                'steps': ["Fetched from WolframAlpha"],
                'source': 'WolframAlpha'
            }
        except Exception as e:
            return None



