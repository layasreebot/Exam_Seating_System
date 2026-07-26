import streamlit as st
import os
import sys

# Add scripts directory to path to import engine
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from assistant_engine import ExamAssistantEngine

# Set page config
st.set_page_config(
    page_title="Exam Seating & Duty Register Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling (sleek dark/light theme elements)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Glassmorphic Container Cards */
    .welcome-card {
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(142, 45, 226, 0.15) 0%, rgba(74, 0, 224, 0.1) 100%);
        border: 1px solid rgba(142, 45, 226, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .welcome-card:hover {
        transform: translateY(-3px);
        border-color: rgba(142, 45, 226, 0.5);
        box-shadow: 0 12px 40px 0 rgba(142, 45, 226, 0.25);
    }
    
    /* Answer Card with Glow */
    .answer-card {
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.12) 0%, rgba(39, 174, 96, 0.08) 100%);
        border: 1px solid rgba(46, 204, 113, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        margin-top: 1rem;
        font-size: 1.1rem;
        color: #f8fafc;
        line-height: 1.6;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .answer-card:hover {
        transform: translateY(-3px);
        border-color: rgba(46, 204, 113, 0.5);
        box-shadow: 0 12px 40px 0 rgba(46, 204, 113, 0.2);
    }
    
    /* Refusal Card */
    .refusal-card {
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(230, 126, 34, 0.12) 0%, rgba(211, 84, 0, 0.08) 100%);
        border: 1px solid rgba(230, 126, 34, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        margin-top: 1rem;
        color: #f8fafc;
        line-height: 1.6;
        transition: all 0.3s ease;
    }
    .refusal-card:hover {
        transform: translateY(-2px);
        border-color: rgba(230, 126, 34, 0.5);
    }

    /* Modern Metric Widget Styling */
    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: linear-gradient(90deg, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        font-weight: 600 !important;
    }
    
    /* Custom Styling for Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Header Gradient Text */
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 50%, #8e2de2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
    }
    
    .subtitle {
        font-size: 1.15rem;
        color: #94a3b8;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Custom Button Animation */
    .stButton button {
        background: linear-gradient(135deg, #4a00e0 0%, #8e2de2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important;
        box-shadow: 0 4px 15px rgba(142, 45, 226, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(142, 45, 226, 0.55) !important;
        background: linear-gradient(135deg, #5c16eb 0%, #9d3bf3 100%) !important;
        border: none !important;
    }
    
    .stButton button:active {
        transform: translateY(1px) !important;
    }

    /* Custom Styling for Suggested Query Tags (rendered inside columns) */
    div[data-testid="column"] button {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #94a3b8 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: none !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 20px !important;
    }
    
    div[data-testid="column"] button:hover {
        background: rgba(142, 45, 226, 0.12) !important;
        color: #ffffff !important;
        border-color: rgba(142, 45, 226, 0.5) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load engine
@st.cache_resource
def get_engine():
    return ExamAssistantEngine()

try:
    engine = get_engine()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# --- SIDEBAR: Database Stats & Quick Demo ---
st.sidebar.markdown("## 📊 Database Statistics")
total_records = len(engine.records)
students_count = len(set(r["student_id"] for r in engine.records if r["student_id"]))
invigilators_count = len(set(r["invigilator"] for r in engine.records if r["invigilator"]))
halls_count = len(set(r["hall"] for r in engine.records if r["hall"]))

st.sidebar.metric("Total Records", total_records)
st.sidebar.metric("Unique Students", students_count)
st.sidebar.metric("Unique Invigilators", invigilators_count)
st.sidebar.metric("Exam Halls", halls_count)

st.sidebar.markdown("---")

st.sidebar.markdown("## 🔑 Quick Demo Login")
st.sidebar.info("Select a user below to log in instantly for testing:")

demo_users = {
    "Select...": "",
    "Student: STU105 (Normal / Absences)": "STU105",
    "Student: STU112 (REC098 - Missing Invigilator)": "STU112",
    "Student: STU114 (REC099 - Missing Seat)": "STU114",
    "Student: STU999 (REC100 - Orphan Christmas)": "STU999",
    "Invigilator: Dr. Ashwini Sekar": "Dr. Ashwini Sekar",
    "Invigilator: Dr. Ashwani Sekar (Similar Name)": "Dr. Ashwani Sekar",
    "Invigilator: Dr. Orphan (REC100 - Christmas)": "Dr. Orphan"
}

demo_selection = st.sidebar.selectbox("Test Accounts", list(demo_users.keys()))
selected_demo_id = demo_users[demo_selection]

# --- MAIN PAGE LAYOUT ---
st.markdown("<div class='main-header'>🎓 Exam Seating & Duty Register Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask questions in plain English about seating assignments, exam schedules, and invigilator duties.</div>", unsafe_allow_html=True)

# Handle Identity Input
st.markdown("### 👤 Step 1: Identify Yourself")
login_col, btn_col = st.columns([4, 1])

with login_col:
    # Pre-fill input if a demo user is selected
    default_login = selected_demo_id if selected_demo_id else ""
    user_identity = st.text_input(
        "Enter your Student ID (e.g. STU105) or Invigilator Name (e.g. Dr. Ashwini Sekar):",
        value=default_login,
        placeholder="Type here..."
    )

# Identity Verification
role, matched_id = engine.identify_user(user_identity)

if not user_identity:
    st.info("Please enter your Student ID or Invigilator Name to access your records.")
elif not role:
    st.error("Error: Identity not recognized.")
    suggestions = engine.get_similar_identities(user_identity)
    if suggestions:
        st.warning("Did you mean one of these?")
        for s in suggestions:
            if st.button(f"Log in as {s}", key=f"btn_{s}"):
                # Extract actual ID/name from suggestion string (e.g. "Student ID: STU105" or "Invigilator: Dr. Ashwini Sekar")
                cleaned_id = s.split(": ", 1)[1]
                st.session_state["custom_login"] = cleaned_id
                st.rerun()
else:
    # User is authenticated
    st.markdown(f"""
    <div class='welcome-card'>
        <h4>Welcome back, <b>{matched_id}</b>!</h4>
        <p>Authenticated Role: <b>{role}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 Step 2: Ask Your Question")
    
    # Clickable Sample Questions for convenience
    supported_qs = engine.get_supported_questions(role)
    st.write("Suggested queries:")
    cols = st.columns(len(supported_qs))
    selected_sample = None
    for idx, q_text in enumerate(supported_qs):
        # Extract the short clean question from suggestion text
        clean_q = q_text.split(" (e.g., '")[1].replace("')", "") if " (e.g., '" in q_text else q_text
        if cols[idx].button(f"🔍 {clean_q}", key=f"q_{idx}"):
            selected_sample = clean_q
            
    # Text input query
    query_placeholder = "e.g., Where is my seat?" if role == "Student" else "e.g., When is my duty?"
    query_value = selected_sample if selected_sample else ""
    
    # We use a text input for the user's question
    user_query = st.text_input(
        "Type your question in plain English:",
        value=query_value,
        placeholder=query_placeholder,
        key="query_input"
    )
    
    if user_query:
        with st.spinner("Processing query..."):
            success, response = engine.answer_query(role, matched_id, user_query)
            
        if success:
            st.markdown(f"""
            <div class='answer-card'>
                <b>Answer:</b><br/>
                {response.replace(chr(10), '<br/>')}
            </div>
            """, unsafe_allow_html=True)
            
            # Show a warning highlight for missing data cases (REC098 / REC099)
            if "[Not Assigned Yet]" in response or "[Unknown" in response:
                st.warning("⚠️ Warning: Some details of your record have not yet been assigned. Please check back later or contact the exam coordinator.")
        else:
            # Not confident (refusal path)
            st.markdown(f"""
            <div class='refusal-card'>
                <b>Assistant:</b><br/>
                {response.replace(chr(10), '<br/>')}
            </div>
            """, unsafe_allow_html=True)
