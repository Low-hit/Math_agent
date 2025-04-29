from knowledge_base import KnowledgeBase
from websearch import WebSearch
from ai_gateway import AIGateway
from feedback import FeedbackCollector
from typing import Dict, Union, List, Optional
import json
import numpy as np
import sympy as sp
from sympy import symbols, solve, diff, integrate, limit, sin, cos, tan, log, exp, pi

class MathAgent:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.websearch = WebSearch()
        self.gateway = AIGateway()
        self.feedback = FeedbackCollector()
        self.x, self.y, self.z = symbols('x y z')
        
    def process_question(self, question: str) -> Dict:
        """Process a mathematical question"""
        # Validate input
        input_validation = self.gateway.validate_input(question)
        if not input_validation['valid']:
            return {
                'error': input_validation['error']
            }
            
        # Try knowledge base first
        kb_result = self.kb.query(question)
        if kb_result:
            # Validate output
            output_validation = self.gateway.validate_output(kb_result['answer'])
            if output_validation['valid']:
                return {
                    'source': 'knowledge_base',
                    'answer': kb_result['answer'],
                    'steps': kb_result['steps'],
                    'similarity': kb_result['similarity']
                }
                
        # If not in knowledge base, try web search
        web_result = self.websearch.search(question)
        if web_result:
            # Validate output
            output_validation = self.gateway.validate_output(web_result['answer'])
            if output_validation['valid']:
                return {
                    'source': 'web_search',
                    'answer': web_result['answer'],
                    'steps': web_result['steps'],
                    'url': web_result['source']
                }
                
        return {
            'error': 'Could not find a suitable answer'
        }
        
    def collect_feedback(self, question: str, answer: Dict, user_feedback: Dict) -> Dict:
        """Collect feedback for a question-answer pair"""
        return self.feedback.collect_feedback(question, answer, user_feedback)

    def solve_equation(self, equation: str) -> Dict:
        """
        Solve a mathematical equation.
        
        Args:
            equation (str): The equation to solve (e.g., "2*x + 3 = 7")
            
        Returns:
            Dict: Solution and steps
        """
        try:
            # Convert string equation to SymPy expression
            eq = sp.sympify("Eq(" + equation.replace("=", ",") + ")")
            solution = solve(eq)
            
            return {
                "equation": equation,
                "solution": solution,
                "steps": ["Parsed equation", "Applied algebraic solving", "Found solution"]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def evaluate_expression(self, expression: str) -> Union[float, str]:
        """
        Evaluate a mathematical expression.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            Union[float, str]: Result of the evaluation or error message
        """
        try:
            result = sp.sympify(expression)
            return float(result) if result.is_number else str(result)
        except Exception as e:
            return f"Error: {str(e)}"
            
    def calculate_derivative(self, expression: str, variable: str = 'x') -> Dict:
        """
        Calculate the derivative of an expression.
        
        Args:
            expression (str): The expression to differentiate
            variable (str): The variable to differentiate with respect to
            
        Returns:
            Dict: Derivative and steps
        """
        try:
            expr = sp.sympify(expression)
            derivative = diff(expr, variable)
            
            return {
                "expression": expression,
                "derivative": str(derivative),
                "steps": [
                    "Parsed expression",
                    f"Calculated derivative with respect to {variable}",
                    "Simplified result"
                ]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def calculate_integral(self, expression: str, variable: str = 'x', 
                         lower_limit: Optional[float] = None, 
                         upper_limit: Optional[float] = None) -> Dict:
        """
        Calculate the integral of an expression.
        
        Args:
            expression (str): The expression to integrate
            variable (str): The variable of integration
            lower_limit (float, optional): Lower limit for definite integral
            upper_limit (float, optional): Upper limit for definite integral
            
        Returns:
            Dict: Integral and steps
        """
        try:
            expr = sp.sympify(expression)
            if lower_limit is not None and upper_limit is not None:
                integral = integrate(expr, (variable, lower_limit, upper_limit))
                integral_type = "definite"
            else:
                integral = integrate(expr, variable)
                integral_type = "indefinite"
                
            return {
                "expression": expression,
                "integral": str(integral),
                "type": integral_type,
                "steps": [
                    "Parsed expression",
                    f"Calculated {integral_type} integral",
                    "Simplified result"
                ]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def calculate_limit(self, expression: str, variable: str = 'x', 
                       point: Union[float, str] = 'oo') -> Dict:
        """
        Calculate the limit of an expression.
        
        Args:
            expression (str): The expression to find the limit of
            variable (str): The variable approaching the limit
            point (float or str): The point the variable approaches
            
        Returns:
            Dict: Limit and steps
        """
        try:
            expr = sp.sympify(expression)
            lim = limit(expr, variable, point)
            
            return {
                "expression": expression,
                "limit": str(lim),
                "steps": [
                    "Parsed expression",
                    f"Calculated limit as {variable} approaches {point}",
                    "Simplified result"
                ]
            }
        except Exception as e:
            return {"error": str(e)}

def main():
    agent = MathAgent()
    
    print("Welcome to the Math Agent!")
    print("Type 'quit' to exit")
    print("Type 'feedback' to see feedback summary")
    
    while True:
        question = input("\nEnter your math question: ")
        
        if question.lower() == 'quit':
            break
            
        if question.lower() == 'feedback':
            summary = agent.feedback.get_feedback_summary()
            print("\nFeedback Summary:")
            print(f"Total feedback collected: {summary['total_feedback']}")
            print(f"Average accuracy: {summary['average_accuracy']:.2f}")
            print(f"Average clarity: {summary['average_clarity']:.2f}")
            print(f"Average relevance: {summary['average_relevance']:.2f}")
            continue
            
        # Process the question
        result = agent.process_question(question)
        
        if 'error' in result:
            print(f"\nError: {result['error']}")
            continue
            
        # Display the answer
        print(f"\nAnswer (from {result['source']}):")
        print(result['answer'])
        
        if result['steps']:
            print("\nSteps:")
            for i, step in enumerate(result['steps'], 1):
                print(f"{i}. {step}")
                
        # Collect feedback
        print("\nPlease provide feedback (1-5):")
        accuracy = int(input("Accuracy (1-5): "))
        clarity = int(input("Clarity (1-5): "))
        relevance = int(input("Relevance (1-5): "))
        comments = input("Comments (optional): ")
        
        feedback = agent.collect_feedback(
            question,
            result,
            {
                'accuracy': accuracy,
                'clarity': clarity,
                'relevance': relevance,
                'comments': comments
            }
        )
        
        print("\nThank you for your feedback!")

if __name__ == "__main__":
    main() 