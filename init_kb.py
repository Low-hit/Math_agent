from knowledge_base import KnowledgeBase

def initialize_knowledge_base():
    kb = KnowledgeBase()
    
    # Basic calculus
    kb.add_entry(
        "What is the derivative of sin(x)?",
        "The derivative of sin(x) is cos(x).",
        [
            "Recall the derivative of sin(x) is a standard result.",
            "The derivative of sin(x) with respect to x is cos(x)."
        ]
    )
    
    kb.add_entry(
        "What is the integral of x^2?",
        "The integral of x^2 is (x^3)/3 + C",
        [
            "Use the power rule for integration",
            "Add 1 to the exponent and divide by the new exponent",
            "Add the constant of integration C"
        ]
    )
    
    # Algebra
    kb.add_entry(
        "What is the quadratic formula?",
        "The quadratic formula is x = (-b ± √(b² - 4ac)) / (2a)",
        [
            "For a quadratic equation ax² + bx + c = 0",
            "The solutions are given by the quadratic formula",
            "The discriminant (b² - 4ac) determines the nature of the roots"
        ]
    )
    
    # Geometry
    kb.add_entry(
        "What is the area of a circle?",
        "The area of a circle is πr²",
        [
            "π (pi) is approximately 3.14159",
            "r is the radius of the circle",
            "Square the radius and multiply by π"
        ]
    )
    
    kb.add_entry(
        "Solve x² + 5x + 6 = 0",
        "The solutions are x = -2 and x = -3.",
        [
            "Factor the quadratic: (x + 2)(x + 3) = 0.",
            "Set each factor to zero: x + 2 = 0 or x + 3 = 0.",
            "Solve for x: x = -2 or x = -3."
        ]
    )
    
    kb.add_entry(
        "What is the derivative of log x?",
        "The derivative of log(x) is 1/x.",
        [
            "Recall the derivative rule for logarithmic functions.",
            "The derivative of log(x) with respect to x is 1/x."
        ]
    )
    
    kb.add_entry(
        "Find the area of a circle with radius 5",
        "The area is 25π square units.",
        [
            "Recall the formula for the area of a circle: A = πr².",
            "Substitute r = 5: A = π * 5² = 25π."
        ]
    )
    
    kb.add_entry(
        "Calculate the integral of x² from 0 to 2",
        "The integral evaluates to 8/3.",
        [
            "Set up the definite integral: ∫₀² x² dx.",
            "The antiderivative of x² is (1/3)x³.",
            "Evaluate from 0 to 2: (1/3)*2³ - (1/3)*0³ = 8/3."
        ]
    )
    
    print("Knowledge base initialized with core questions.")

if __name__ == "__main__":
    initialize_knowledge_base() 