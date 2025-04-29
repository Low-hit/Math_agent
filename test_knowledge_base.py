import json
from knowledge_base import KnowledgeBase

def load_test_questions(file_path='jee_questions.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Initialize knowledge base
    print("Initializing knowledge base...")
    kb = KnowledgeBase()
    
    # Load test questions
    try:
        questions = load_test_questions()
    except FileNotFoundError:
        print("Error: jee_questions.json not found!")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in jee_questions.json!")
        return
    
    print(f"\nTesting {len(questions)} questions...\n")
    print("-" * 80)
    
    # Test each question
    for i, q_data in enumerate(questions, 1):
        question = q_data['text']
        expected_answer = q_data['expected_answer']
        
        # Query the knowledge base
        results = kb.query(question)
        
        print(f"Test Case {i}:")
        print(f"Question: {question}")
        print(f"Expected Answer: {expected_answer}")
        print("\nKnowledge Base Response:")
        
        if results:
            for j, (similarity, answer, steps) in enumerate(results[:3], 1):
                print(f"\nMatch {j} (Similarity: {similarity:.3f}):")
                print(f"Answer: {answer}")
                print("Steps:")
                for step in steps:
                    print(f"- {step}")
        else:
            print("No matching responses found")
            
        print("\n" + "-" * 80)

if __name__ == "__main__":
    main() 