import streamlit as st
from PIL import Image
import io

# Backend Integrations
import vision
import pdf_utils
import material_utils
import rag

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Clarivo | AI Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS INJECTION (STRICT PREMIUM)
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');

        /* Ultra-Dark Background */
        .stApp {
            background-color: #000000;
            font-family: 'Inter', sans-serif !important;
            color: #A0A0A0;
        }
        
        /* Force All Headings to Inter (Clean Sans-Serif) */
        h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown li, .stMarkdown span {
            font-family: 'Inter', sans-serif !important;
        }

        h1, h2, h3 {
            color: #E6E1C5 !important;
            font-weight: 400 !important;
            letter-spacing: -0.01em !important;
        }

        h4, h5, h6 {
            color: #FFFFFF !important;
            font-weight: 400 !important;
        }

        /* Fix Sidebar Toggle: Make header transparent instead of hidden */
        header {
            background-color: transparent !important;
        }
        footer {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }

        /* Typography Classes */
        .eyebrow {
            font-size: 0.70rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #666666;
            margin-bottom: -15px;
        }
        
        /* The ONLY element using the classic Serif font (Size increased) */
        .wordmark {
            font-size: 4.8rem;
            color: #E6E1C5;
            font-family: 'Cormorant Garamond', serif !important;
            letter-spacing: -0.02em;
            font-weight: 500;
            margin-bottom: 5px;
            margin-top: -10px;
        }
        
        .tagline {
            font-size: 1rem !important;
            color: #A0A0A0 !important;
            font-weight: 300 !important;
            margin-bottom: 30px !important;
        }
        
        .overview-heading {
            font-size: 2.5rem !important;
            line-height: 1.4 !important;
            color: #E6E1C5 !important;
            font-weight: 400 !important;
            margin-top: 0.5rem !important;
            margin-bottom: 1.5rem !important;
        }

        /* Subtle Hairline Dividers */
        hr {
            border-top: 1px solid #1A1A1A !important;
            margin: 2rem 0 !important;
        }

        /* Container / Card Reskin */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #080808 !important;
            border: 1px solid #1A1A1A !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }

        /* File Uploader Clean Reskin */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #0A0A0A !important;
            border: 1px dashed #262626 !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background-color: #1A1A1A !important;
            color: #E6E1C5 !important;
            border: none !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #040404 !important;
            border-right: 1px solid #1A1A1A !important;
        }

        /* STRICT Button Styling */
        div[data-testid="stButton"] button {
            background-color: #E6E1C5 !important;
            border-color: #E6E1C5 !important;
            border-radius: 6px !important;
            padding: 0.6rem 2rem !important;
            border: none !important;
            transition: opacity 0.3s ease !important;
        }
        div[data-testid="stButton"] button p {
            color: #000000 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
        }
        div[data-testid="stButton"] button:hover {
            opacity: 0.8 !important;
            background-color: #E6E1C5 !important;
            border-color: #E6E1C5 !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background-color: transparent !important;
            border-bottom: 1px solid #1A1A1A !important;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border: none !important;
            padding: 1rem 0 !important;
            color: #666666 !important;
            font-size: 0.9rem !important;
            font-weight: 400 !important;
            transition: color 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            color: #E6E1C5 !important;
            border-bottom: 1px solid #E6E1C5 !important;
        }

        /* Custom Bullet List */
        .custom-list-item {
            padding: 1rem 0;
            border-bottom: 1px solid #151515;
            color: #B0B0B0;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
        }
        .custom-list-item::before {
            content: "•";
            color: #E6E1C5;
            font-size: 1.2rem;
            margin-right: 12px;
            line-height: 1;
        }
        .custom-list-item:last-child {
            border-bottom: none;
        }

        /* Data Display Classes */
        .metric-label {
            color: #666666;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.2rem;
        }
        
        .metric-value {
            color: #FFFFFF;
            font-size: 1.2rem;
            font-weight: 400;
        }

        .section-header {
            color: #E6E1C5;
            font-size: 1.3rem;
            font-weight: 400;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .info-box {
            background-color: #080808;
            border: 1px solid #1A1A1A;
            border-radius: 8px;
            padding: 1.5rem;
            color: #A0A0A0;
            font-size: 0.95rem;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
def init_session_state():
    if 'material_context' not in st.session_state:
        st.session_state.material_context = None
    if 'extracted_info' not in st.session_state:
        st.session_state.extracted_info = None
    if 'teaching_plan' not in st.session_state:
        st.session_state.teaching_plan = None
    if 'last_homework_name' not in st.session_state:
        st.session_state.last_homework_name = None

def reset_analysis_state():
    st.session_state.extracted_info = None
    st.session_state.teaching_plan = None

# ==========================================
# RENDER: HEADER
# ==========================================
def render_header():
    st.markdown('<div class="wordmark">Clarivo</div>', unsafe_allow_html=True)
    # Updated Tagline
    st.markdown('<div class="tagline">A calm, guided way for parents to teach, verify, and understand their child\'s assignments.</div>', unsafe_allow_html=True)

# ==========================================
# RENDER: SIDEBAR
# ==========================================
def render_sidebar():
    with st.sidebar:
        # Changed "Settings" to "OPTIONAL"
        st.markdown('<div class="eyebrow" style="text-align:left;">OPTIONAL</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size:1.1rem; margin-top:20px; color:#FFFFFF !important;'>Course Material</h3>", unsafe_allow_html=True)
        st.markdown("""
            <p style="font-size: 0.85rem; margin-bottom: 1.5rem; color:#888888;">
            Upload the textbook or curriculum PDF for this subject, so explanations and answers stay grounded in it.
            </p>
        """, unsafe_allow_html=True)
        
        material_file = st.file_uploader("Upload Document", type=["pdf"], label_visibility="collapsed")
        
        if material_file:
            with st.spinner("Processing framework..."):
                file_bytes = material_file.read()
                st.session_state.material_context = material_utils.extract_text_from_material_pdf(file_bytes)
            st.markdown('<div style="color:#E6E1C5; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; margin-top:1rem;">Material uploaded successfully</div>', unsafe_allow_html=True)

# ==========================================
# RENDER: OVERVIEW TAB
# ==========================================
def render_overview_tab():
    col_text, col_list = st.columns([1.2, 1], gap="large")
    
    with col_text:
        # Updated Overview Heading
        st.markdown('<div class="overview-heading">Empowering parents,<br>Guiding students,<br>and building confidence.</div>', unsafe_allow_html=True)
        
    with col_list:
        # Updated Overview Text
        st.markdown("""
            <p style='color:#A0A0A0; font-size:0.95rem; margin-bottom:2rem; margin-top:1rem;'>
            Clarivo transforms the way you help your children with their homework. We provide structured, pedagogical guidance rather than just handing out the answers.
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="custom-list-item">AI-driven context extraction from everyday homework</div>
            <div class="custom-list-item">Step-by-step parent guides aligned with school curriculums</div>
            <div class="custom-list-item">Clear frameworks designed for long-term student comprehension</div>
        """, unsafe_allow_html=True)

# ==========================================
# RENDER: WORKSPACE TAB
# ==========================================
def render_workspace_tab():
    col_left, col_right = st.columns([1, 1.2], gap="large")
    
    with col_left:
        with st.container(border=True):
            st.markdown("<h3 style='font-size:1.3rem;'>Input Parameters</h3>", unsafe_allow_html=True)
            st.write("Provide the assignment document for structural analysis. Ensure the following criteria are met for optimal processing.")
            st.markdown("""
                <div class="custom-list-item" style="padding: 0.6rem 0; font-size: 0.85rem;">High-contrast image quality</div>
                <div class="custom-list-item" style="padding: 0.6rem 0; font-size: 0.85rem;">Complete document capture</div>
                <div class="custom-list-item" style="padding: 0.6rem 0; font-size: 0.85rem;">PDF format for multi-page data</div>
            """, unsafe_allow_html=True)

    with col_right:
        with st.container(border=True):
            st.markdown('<div class="metric-label" style="margin-bottom:10px;">Document Upload</div>', unsafe_allow_html=True)
            hw_file = st.file_uploader("Upload File", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
            
            if hw_file and hw_file.name != st.session_state.last_homework_name:
                st.session_state.last_homework_name = hw_file.name
                reset_analysis_state()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Process Document", type="primary", use_container_width=True):
                if hw_file:
                    with st.spinner("Extracting structural data..."):
                        file_ext = hw_file.name.split('.')[-1].lower()
                        if file_ext == 'pdf':
                            images = pdf_utils.pdf_to_images(hw_file.read())
                            st.session_state.extracted_info = vision.extract_homework_details_from_pages(images)
                        else:
                            image = Image.open(hw_file)
                            st.session_state.extracted_info = vision.extract_homework_details(image)
                else:
                    st.markdown('<div style="color:#666666; font-size:0.85rem; margin-top:10px;">Input required</div>', unsafe_allow_html=True)

    if st.session_state.extracted_info:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Extracted Parameters</div>', unsafe_allow_html=True)
        
        info = st.session_state.extracted_info
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True):
                st.markdown('<div class="metric-label">Subject Context</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{info.get("subject", "N/A")}</div>', unsafe_allow_html=True)
        with m2:
            with st.container(border=True):
                st.markdown('<div class="metric-label">Topic Classification</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{info.get("topic", "N/A")}</div>', unsafe_allow_html=True)
        with m3:
            with st.container(border=True):
                st.markdown('<div class="metric-label">Estimated Level</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{info.get("grade_level", "N/A")}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for idx, q in enumerate(info.get("questions", [])):
            with st.container(border=True):
                st.markdown(f'<div class="metric-label">Query {idx + 1}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:#D0D0D0; font-size:0.95rem;">{q}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Pedagogical Strategy", type="primary"):
            with st.spinner("Synthesizing strategic response..."):
                st.session_state.teaching_plan = rag.generate_teaching_plan(
                    st.session_state.extracted_info, 
                    st.session_state.material_context
                )

    if st.session_state.teaching_plan:
        plan = st.session_state.teaching_plan
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header" style="font-size:1.8rem;">Strategic Framework</div>', unsafe_allow_html=True)
        
        o1, o2 = st.columns(2)
        with o1:
            with st.container(border=True):
                st.markdown('<div class="metric-label">Duration Estimate</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{plan.get("estimated_time", "N/A")}</div>', unsafe_allow_html=True)
        with o2:
            with st.container(border=True):
                st.markdown('<div class="metric-label">Complexity Index</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{plan.get("difficulty", "N/A")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Instructional Blueprint</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-box">{plan.get("parent_explanation", "Data unavailable.")}</div>', unsafe_allow_html=True)

        col_mistakes, col_activity = st.columns(2, gap="large")
        with col_mistakes:
            st.markdown('<div class="section-header">Risk Analysis</div>', unsafe_allow_html=True)
            for mistake in plan.get("common_mistakes", []):
                st.markdown(f'<div class="custom-list-item" style="padding:0.6rem 0;">{mistake}</div>', unsafe_allow_html=True)

        with col_activity:
            st.markdown('<div class="section-header">Practical Application</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color:#A0A0A0; font-size:0.95rem; line-height:1.6;">{plan.get("daily_activity", "Data unavailable.")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-header">Resolution & Rationale</div>', unsafe_allow_html=True)
        for idx, ans in enumerate(plan.get("answers", [])):
            with st.container(border=True):
                st.markdown(f'<div class="metric-label">Item {idx + 1}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:#FFFFFF; font-size:1.05rem; margin-bottom:1rem;">{ans.get("question", "")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div><strong style="color:#E6E1C5; font-weight:500; font-size:0.9rem;">OUTPUT:</strong> <span style="color:#D0D0D0; font-size:0.95rem;">{ans.get("answer", "")}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:0.4rem;"><strong style="color:#E6E1C5; font-weight:500; font-size:0.9rem;">LOGIC:</strong> <span style="color:#D0D0D0; font-size:0.95rem;">{ans.get("explanation", "")}</span></div>', unsafe_allow_html=True)

        resource = plan.get("resource_link")
        if resource:
            st.markdown('<div class="section-header">External Documentation</div>', unsafe_allow_html=True)
            st.markdown(f"<a href='{resource}' target='_blank' style='color:#E6E1C5; text-decoration:none; border-bottom:1px solid #E6E1C5; padding-bottom:2px; font-size:0.85rem;'>Access Reference Document</a>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# MAIN APP EXECUTION
# ==========================================
def main():
    init_session_state()
    inject_custom_css()
    render_header()
    render_sidebar()
    
    tab1, tab2 = st.tabs(["Overview", "Workspace"])
    
    with tab1:
        render_overview_tab()
        
    with tab2:
        render_workspace_tab()

if __name__ == "__main__":
    main()