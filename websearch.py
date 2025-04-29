import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Dict, Any
import logging

class WebSearch:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_math_content(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for mathematical content on educational websites.
        """
        try:
            # Search on Wolfram Alpha API (requires API key)
            # For now, we'll use a simple web search
            search_url = f"https://www.google.com/search?q={query}+site:math.stackexchange.com+OR+site:brilliant.org+OR+site:khanacademy.org"
            
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant content
            results = []
            for result in soup.find_all('div', class_='g'):
                title = result.find('h3')
                snippet = result.find('div', class_='VwiC3b')
                
                if title and snippet:
                    results.append({
                        'title': title.text,
                        'snippet': snippet.text
                    })
            
            if not results:
                return None
            
            # Extract mathematical content
            math_content = self._extract_math_content(results)
            
            return {
                'success': True,
                'content': math_content,
                'source': 'Web Search'
            }
            
        except Exception as e:
            self.logger.error(f"Error in web search: {str(e)}")
            return None
    
    def _extract_math_content(self, results: list) -> str:
        """
        Extract mathematical content from search results.
        """
        math_patterns = [
            r'\$\$.*?\$\$',  # LaTeX math
            r'\$.*?\$',      # Inline math
            r'[0-9+\-*/=()\[\]]+',  # Basic math expressions
            r'sin|cos|tan|log|ln|sqrt',  # Common functions
        ]
        
        math_content = []
        for result in results:
            text = f"{result['title']} {result['snippet']}"
            if any(re.search(pattern, text) for pattern in math_patterns):
                math_content.append(text)
        
        return '\n\n'.join(math_content)
    
    def validate_math_content(self, content: str) -> bool:
        """
        Validate if the content contains legitimate mathematical information.
        """
        # Check for mathematical patterns
        math_patterns = [
            r'\d+',  # Numbers
            r'[+\-*/=]',  # Basic operators
            r'[a-zA-Z]',  # Variables
            r'[()\[\]]',  # Parentheses
            r'sin|cos|tan|log|ln|sqrt',  # Common functions
        ]
        
        return any(re.search(pattern, content) for pattern in math_patterns) 