from typing import Dict, List, Optional
import json
import os
from difflib import SequenceMatcher

class KnowledgeBase:
    def __init__(self):
        self.kb_file = 'math_kb.json'
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict:
        """Load the knowledge base from file"""
        if os.path.exists(self.kb_file):
            with open(self.kb_file, 'r') as f:
                return json.load(f)
        return {}
        
    def _save_knowledge_base(self):
        """Save the knowledge base to file"""
        with open(self.kb_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
            
    def _similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
        
    def add_entry(self, question: str, answer: str, steps: List[str]):
        """Add a new entry to the knowledge base"""
        self.knowledge_base[question] = {
            'answer': answer,
            'steps': steps
        }
        self._save_knowledge_base()
        
    def query(self, question: str, threshold: float = 0.85) -> Optional[Dict]:
        """Query the knowledge base for similar questions"""
        if not self.knowledge_base:
            return None
            
        # Find the most similar question
        best_match = None
        best_similarity = 0
        
        for stored_question in self.knowledge_base:
            similarity = self._similarity(question, stored_question)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = stored_question
                
        if best_similarity < threshold:
            return None
            
        return {
            'question': best_match,
            'answer': self.knowledge_base[best_match]['answer'],
            'steps': self.knowledge_base[best_match]['steps'],
            'similarity': best_similarity
        } 