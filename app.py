import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR AESTHETIC UI ---
# Glassmorphism, sleek modern fonts, and dark theme variables
st.markdown("""
<style>
/* Base theme and font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background gradient blobs */
.stApp {
    background-color: #0B0F19;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(76, 29, 149, 0.15), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(14, 165, 233, 0.15), transparent 25%);
    background-attachment: fixed;
    color: #F1F5F9;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Header style styling */
h1, h2, h3, h4, h5, h6 {
    color: #F8FAFC !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

h1 {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 0.2rem;
}

/* Custom Containers (glassmorphism) */
.glass-container {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    margin-bottom: 24px;
}

/* Custom st.button styling */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366F1 0%, #3B82F6 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
}

/* Text area styling */
.stTextArea > div > div > textarea {
    background-color: rgba(15, 23, 42, 0.6) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 1px #38BDF8 !important;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    color: #38BDF8 !important;
}

/* Spinner */
.stSpinner > div > div {
    border-top-color: #38BDF8 !important;
}

</style>
""", unsafe_allow_html=True)

# Application Header
st.title("✨ AI Code Reviewer")
st.markdown("<p style='font-size: 1.1rem; color: #94A3B8; margin-top: -10px; margin-bottom: 30px;'>Elevate your code quality with AI-driven bug detection and optimization.</p>", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 🤖 Model Options")
    model_choice = st.selectbox("Select Model", ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"])
    
    st.markdown("---")
    st.markdown("### 📝 About")
    st.info("This application uses Google's Gemini models to analyze your code, find potential bugs, and suggest performance optimizations similar to LeetAI of LeetCode.")

# Main dual-column layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("### 💻 Source Code")
    language_choice = st.selectbox("Select Programming Language:", ["Python", "JavaScript", "TypeScript", "C++", "Java", "Go", "Rust", "Other"])
    code_input = st.text_area("Paste your code here for review:", height=320, placeholder="# Write or paste your code here...")
    
    analyze_btn = st.button("🚀 Analyze Code")
    st.markdown("</div>", unsafe_allow_html=True)

# Establish API Key
API_KEY = os.getenv("GEMINI_API_KEY")

def review_code(code: str, language: str, model_name: str, api_key: str):
    """Call the Gemini API to review the provided code."""
    try:
        genai.configure(api_key=api_key)
        
        # Configure the model using standard or system instruction
        # Note: system_instruction is supported specifically in gemini-1.5 models.
        kwargs = {}
        if "2.5" in model_name or "2.0" in model_name:
            kwargs["system_instruction"] = (
                "You are an expert software engineer and code reviewer like LEECO.ai. Your task is to analyze the provided code. "
                "1. Identify any bugs or syntax errors. "
                "2. Suggest optimizations for better performance, readability, and maintainability. "
                "3. Provide the corrected/optimized version of the code. "
                "4. Keep the review concise, structured, and use Markdown for formatting."
            )
            model = genai.GenerativeModel(model_name=model_name, **kwargs)
            prompt = f"Please review the following {language} snippet:\n\n```\n{code}\n```\n\nProvide a detailed code review, pointing out bugs and optimizations."
        else:
            model = genai.GenerativeModel(model_name=model_name)
            prompt = (
                "You are an expert software engineer and code reviewer like LEECO.ai. Address these points:\n"
                "1. Identify any bugs or syntax errors.\n"
                "2. Suggest optimizations for better performance and readability.\n"
                "3. Provide the corrected/optimized code.\n\n"
                f"Review the following {language} code:\n\n```\n{code}\n```"
            )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"**Error executing AI Review:** {str(e)}"

with col2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("### 📋 Review Report")
    
    if analyze_btn:
        if not code_input.strip():
            st.warning("⚠️ Please provide some code to review.")
        elif not API_KEY:
            st.error("🔑 Please set the GEMINI_API_KEY variable in your .env file.")
        else:
            with st.spinner("Analyzing your code snippet..."):
                report = review_code(code_input, language_choice, model_choice, API_KEY)
                
            st.markdown(report)
    else:
        st.markdown("<div style='text-align: center; color: #64748B; padding: 40px 0;'>Paste code and click Analyze to see the AI review here.</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
