import streamlit as st
from knowledge_base import KnowledgeBase
from router import WebSearch
from router import Router
from feedback import FeedbackLogger
from guardrails import Guardrails
import time

# Page configuration
st.set_page_config(
    page_title="Math Agent",
    page_icon="🧮",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.2rem;
    }
    .feedback-btn {
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    kb = KnowledgeBase()
    websearch = WebSearch(app_id="7A5QRH-QWGRXU6QKU")
    router = Router(kb, websearch)
    feedback_logger = FeedbackLogger()
    guardrails = Guardrails()
    return kb, websearch, router, feedback_logger, guardrails

kb, websearch, router, feedback_logger, guardrails = init_components()

# Header
st.title("🧮 Math Agent")
st.markdown("""
    ### Your Intelligent Mathematics Assistant
    Ask any mathematics question - from basic arithmetic to advanced calculus!
""")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
        This Math Agent can help you with:
        - Basic arithmetic
        - Algebra
        - Calculus
        - Geometry
        - Trigonometry
        - And more!
        
        The agent uses a combination of:
        1. Knowledge Base
        2. Web Search
        3. Symbolic Mathematics
    """)
    
    st.header("Sample Questions")
    st.markdown("""
        Try these examples:
        - What is the derivative of sin(x)?
        - Solve x² + 5x + 6 = 0
        - Find the area of a circle with radius 5
        - Calculate ∫x²dx from 0 to 2
    """)

# Main content
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # User input
    user_input = st.text_input(
        "Enter your math question:",
        placeholder="e.g., What is the derivative of sin(x)?"
    )

    if user_input:
        # Input validation through guardrails
        is_valid, error_msg = guardrails.input_guardrail(user_input)
        
        if not is_valid:
            st.error(f"⚠️ {error_msg}")
        else:
            with st.spinner("Thinking..."):
                # Add slight delay for better UX
                time.sleep(0.5)
                try:
                    response = router.route(user_input)
                    
                    # Store in session state
                    st.session_state['last_question'] = user_input
                    st.session_state['last_response'] = response
                    
                    # Display answer
                    st.markdown("### Answer")
                    st.markdown(f"{response['answer']}")
                    
                    if 'steps' in response:
                        st.markdown("### Steps")
                        for i, step in enumerate(response['steps'], 1):
                            st.markdown(f"{i}. {step}")
                            
                    if 'source' in response:
                        st.info(f"Source: {response['source']}")
                    
                    # Feedback section
                    st.markdown("### Was this answer helpful?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 Yes", key="yes"):
                            feedback_logger.log_feedback(user_input, response, True)
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👎 No", key="no"):
                            feedback = st.text_area("What was wrong or missing?")
                            if feedback:
                                feedback_logger.log_feedback(user_input, response, False, feedback)
                                st.info("Thank you for your feedback!")
                                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)} ")

with main_col2:
    if 'last_response' in st.session_state and st.session_state['last_response']:
        st.markdown("### Previous Question")
        st.markdown(f"Q: {st.session_state['last_question']}")
        
        # Display feedback stats if available
        stats = feedback_logger.get_improvements()
        if stats:
            st.markdown("### Feedback Statistics")
            st.markdown(f"Total questions answered: {len(stats)}")
            # Add more stats as needed

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Lohith Sai Beeram") 