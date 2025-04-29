from datetime import datetime
from typing import Optional, Dict, Any, List
import json
from transformers import pipeline
import dspy
from pydantic import BaseModel
import os
import logging

class FeedbackResponse(BaseModel):
    correctness: float  # 0-1 score
    clarity: float     # 0-1 score
    helpfulness: float # 0-1 score
    comments: str      # Free-form feedback

class MathFeedback(dspy.Module):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # Define DSPy signatures
        self.generate_feedback = dspy.ChainOfThought("question, answer -> feedback")
        self.analyze_feedback = dspy.ChainOfThought("feedback, question, answer -> improvements")
        
    def collect_feedback(self, question: str, answer: str) -> Dict[str, Any]:
        """
        Collect feedback on the answer quality.
        """
        try:
            # Generate feedback using DSPy
            feedback = self.generate_feedback(
                question=question,
                answer=answer
            )
            
            # Analyze feedback for improvements
            improvements = self.analyze_feedback(
                feedback=feedback.feedback,
                question=question,
                answer=answer
            )
            
            return {
                'success': True,
                'feedback': feedback.feedback,
                'improvements': improvements.improvements,
                'source': 'DSPy Feedback'
            }
            
        except Exception as e:
            self.logger.error(f"Error in feedback collection: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_knowledge(self, feedback: Dict[str, Any]) -> bool:
        """
        Update knowledge base based on feedback.
        """
        try:
            if not feedback['success']:
                return False
            
            # Extract key information from feedback
            improvements = feedback['improvements']
            
            # Update knowledge base with improvements
            # This would typically involve updating the vector database
            # For now, we'll just log the improvements
            self.logger.info(f"Knowledge base updates suggested: {improvements}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating knowledge: {str(e)}")
            return False

class FeedbackCollector:
    def __init__(self):
        self.feedback_file = 'feedback.json'
        self.feedback = self._load_feedback()
        
    def _load_feedback(self) -> Dict:
        """Load feedback from file"""
        if os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        return {'entries': []}
        
    def _save_feedback(self):
        """Save feedback to file"""
        with open(self.feedback_file, 'w') as f:
            json.dump(self.feedback, f, indent=2)
            
    def collect_feedback(self, question: str, answer: Dict, user_feedback: Dict) -> Dict:
        """Collect feedback for a question-answer pair"""
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer,
            'user_feedback': {
                'accuracy': user_feedback.get('accuracy', 0),
                'clarity': user_feedback.get('clarity', 0),
                'relevance': user_feedback.get('relevance', 0),
                'comments': user_feedback.get('comments', '')
            }
        }
        
        self.feedback['entries'].append(feedback_entry)
        self._save_feedback()
        
        return feedback_entry
        
    def get_feedback_summary(self) -> Dict:
        """Get summary statistics of feedback"""
        if not self.feedback['entries']:
            return {
                'total_feedback': 0,
                'average_accuracy': 0,
                'average_clarity': 0,
                'average_relevance': 0
            }
            
        total = len(self.feedback['entries'])
        accuracy_sum = sum(entry['user_feedback']['accuracy'] for entry in self.feedback['entries'])
        clarity_sum = sum(entry['user_feedback']['clarity'] for entry in self.feedback['entries'])
        relevance_sum = sum(entry['user_feedback']['relevance'] for entry in self.feedback['entries'])
        
        return {
            'total_feedback': total,
            'average_accuracy': accuracy_sum / total,
            'average_clarity': clarity_sum / total,
            'average_relevance': relevance_sum / total
        }
        
    def get_recent_feedback(self, limit: int = 5) -> List[Dict]:
        """Get recent feedback entries"""
        return self.feedback['entries'][-limit:]

class FeedbackLogger:
    def __init__(self, log_file="feedback_log.txt"):
        self.log_file = log_file
        self.analyzer = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self._load_feedback_history()

    def _load_feedback_history(self):
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                self.feedback_history = [line.strip().split("\t") for line in f]
        except FileNotFoundError:
            self.feedback_history = []

    def log_feedback(self, question: str, response: str, is_helpful: bool, comment: Optional[str] = None):
        timestamp = datetime.now().isoformat()
        feedback_entry = f"{timestamp}\tQ: {question}\tA: {response}\tHelpful: {is_helpful}\tComment: {comment or ''}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(feedback_entry)
        
        self.feedback_history.append(feedback_entry.strip().split("\t"))
        self._analyze_feedback(question, response, is_helpful, comment)

    def _analyze_feedback(self, question: str, response: str, is_helpful: bool, comment: Optional[str] = None):
        """Analyze feedback using a local model to improve future responses."""
        feedback_text = f"Helpful: {is_helpful}"
        if comment:
            feedback_text += f", Comment: {comment}"

        # Analyze the sentiment of the feedback
        sentiment = self.analyzer(feedback_text)[0]
        
        # Store analysis for future improvements
        self._store_analysis({
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"],
            "feedback": feedback_text,
            "question": question,
            "response": response
        })

    def _store_analysis(self, analysis):
        """Store the analysis results for future reference."""
        analysis_file = "feedback_analysis.json"
        try:
            with open(analysis_file, "r", encoding="utf-8") as f:
                existing_analysis = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_analysis = []

        existing_analysis.append({
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        })

        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(existing_analysis, f, indent=2)

    def get_improvements(self) -> list:
        """Get the latest improvements based on feedback analysis."""
        try:
            with open("feedback_analysis.json", "r", encoding="utf-8") as f:
                analysis_data = json.load(f)
                return [item["analysis"] for item in analysis_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return [] 