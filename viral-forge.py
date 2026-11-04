import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="ViralForge", page_icon="⚡", layout="centered")

# ==================== CLEAN, SAFE CSS ====================
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 820px;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 700;
    }
    p, label, .stMarkdown, .stCaption {
        color: #1e293b !important;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.3rem;
        border: none;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99,102,241,0.3);
    }
    .result-card {
        background: #ffffff;
        padding: 1.1rem 1.3rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 0.9rem;
        color: #0f172a;
    }
    .result-card small {
        color: #64748b;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * {
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "ideas" not in st.session_state:
    st.session_state.ideas = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚡ ViralForge")
    st.caption("Simple idea generator")
    st.divider()

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="Paste your API key"
    )
    if api_key:
        st.session_state.api_key = api_key
        try:
            genai.configure(api_key=api_key)
            st.success("Connected")
        except Exception:
            st.error("Invalid key")

    model = st.selectbox(
        "Model",
        ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-4-argon"],
        index=0
    )

# ==================== MAIN ====================
st.title("ViralForge")
st.markdown("Generate scroll-stopping content ideas, then download them as CSV or PDF.")

if not st.session_state.api_key:
    st.info("Add your Gemini API key in the sidebar to get started.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("Niche", placeholder="e.g. Personal finance for Gen Z")
    platform = st.selectbox("Platform", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X"])
with col2:
    style = st.selectbox("Style", ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes"])
    num_ideas = st.slider("Number of ideas", 3, 10, 5)

if st.button("Generate Ideas", type="primary", use_container_width=True) and niche:
    with st.spinner("Generating ideas..."):
        try:
            model_obj = genai.GenerativeModel(model)
            prompt = f"""
            Generate {num_ideas} highly scroll-stopping content ideas for {platform} in the niche: "{niche}".
            Style: {style}.
            
            Each idea must have a strong hook in the first 1-3 seconds.
            Make them specific, emotional or valuable, and optimized for {platform}.
            Keep each idea to 1-2 short sentences.
            
            Format as a clean numbered list only.
            """
            response = model_obj.generate_content(prompt)
            ideas_text = response.text.strip()

            lines = [line.strip() for line in ideas_text.split("\n") if line.strip() and any(c.isdigit() for c in line[:3])]
            new_ideas = []
            for line in lines[:num_ideas]:
                clean = line.split(".", 1)[-1].strip() if "." in line else line
                new_ideas.append({
                    "idea": clean,
                    "platform": platform,
                    "niche": niche,
                    "style": style,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })

            st.session_state.ideas = new_ideas
            st.success("Ideas ready")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display results
if st.session_state.ideas:
    st.markdown("### Generated Ideas")
    for i, idea in enumerate(st.session_state.ideas, 1):
        st.markdown(f"""
        <div class="result-card">
            <strong>{i}.</strong> {idea['idea']}<br>
            <small>{idea['platform']} · {idea['style']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Download")

    df = pd.DataFrame(st.session_state.ideas)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="viralforge_ideas.csv",
        mime="text/csv",
        use_container_width=True
    )

    def create_pdf(ideas):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "ViralForge Content Ideas", ln=True, align="C")
        pdf.ln(6)
        pdf.set_font("Helvetica", size=11)
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        pdf.ln(8)

        for i, idea in enumerate(ideas, 1):
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 8, f"{i}. {idea['idea']}")
            pdf.set_font("Helvetica", size=10)
            pdf.cell(0, 6, f"Platform: {idea['platform']}  |  Style: {idea['style']}", ln=True)
            pdf.ln(5)

        return bytes(pdf.output())

    pdf_bytes = create_pdf(st.session_state.ideas)
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="viralforge_ideas.pdf",
        mime="application/pdf",
        use_container_width=True
    )

else:
    st.info("Enter a niche and click **Generate Ideas** to begin.")
