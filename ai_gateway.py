import re
from typing import Optional, Dict, Any
import logging

class AIGateway:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.math_patterns = [
            r'\b(derivative|integral|limit|solve|equation|function|matrix|vector|calculus|algebra|geometry|trigonometry)\b',
            r'[0-9+\-*/^()\[\]{}]',
            r'\b(sin|cos|tan|cot|sec|csc|log|ln|exp)\b'
        ]
        
    def validate_input(self, query: str) -> Dict[str, Any]:
        """Validate if the input is a mathematical question"""
        # Check if the query contains mathematical content
        is_math = any(re.search(pattern, query.lower()) for pattern in self.math_patterns)
        
        if not is_math:
            return {
                "valid": False,
                "error": "Input does not appear to be a mathematical question"
            }
            
        # Check for potentially harmful content
        if any(word in query.lower() for word in ["hack", "exploit", "bypass", "security"]):
            return {
                "valid": False,
                "error": "Input contains potentially harmful content"
            }
            
        return {
            "valid": True,
            "query": query
        }
    
    def validate_output(self, response: str) -> Dict[str, Any]:
        """Validate the response for correctness and safety"""
        # Check if response is empty
        if not response.strip():
            return {
                "valid": False,
                "error": "Empty response"
            }
            
        # Check for error messages in response
        if "error" in response.lower():
            return {
                "valid": False,
                "error": "Response contains error"
            }
            
        return {
            "valid": True,
            "response": response
        }
    
    def process_input(self, input_text: str) -> Optional[str]:
        """
        Process input through the gateway.
        """
        validation = self.validate_input(input_text)
        
        if not validation["valid"]:
            self.logger.warning(f"Invalid input: {validation['error']}")
            return None
        
        return input_text
    
    def process_output(self, output_text: str) -> Optional[str]:
        """
        Process output through the gateway.
        """
        validation = self.validate_output(output_text)
        
        if not validation["valid"]:
            self.logger.warning(f"Invalid output: {validation['error']}")
            return None
        
        return output_text 