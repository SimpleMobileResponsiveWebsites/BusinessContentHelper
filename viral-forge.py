import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import google.generativeai as genai

st.set_page_config(
    page_title="ViralForge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FIXED MODERN CSS ====================
st.markdown("""
<style>
    /* Base app */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0f172a;
    }

    /* Sidebar - keep light text on dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Main content text */
    .main h1, .main h2, .main h3, .main p, .main li, .main span {
        color: #0f172a !important;
    }

    /* Metrics - force readable labels + values */
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    [data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 500;
        font-size: 0.875rem;
    }
    [data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700;
    }
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
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

    /* Inputs */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        color: #0f172a !important;
        background: white;
    }

    /* Info / success boxes */
    .stInfo, .stSuccess, .stWarning {
        border-radius: 12px;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# ⚡ ViralForge")
st.sidebar.caption("Forge your viral page")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Content Idea Generator", "Post Planner", "Analytics Tracker", 
     "Brand Deal Pitch", "Growth Playbook"],
    label_visibility="collapsed"
)

# Session state
if "posts" not in st.session_state:
    st.session_state.posts = []
if "followers" not in st.session_state:
    st.session_state.followers = 1200
if "engagement_rate" not in st.session_state:
    st.session_state.engagement_rate = 4.8
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Gemini Key
st.sidebar.markdown("### 🔑 Gemini API")
api_key_input = st.sidebar.text_input(
    "API Key",
    type="password",
    value=st.session_state.gemini_api_key,
    placeholder="Paste your Gemini key",
    help="Get free key → aistudio.google.com/app/apikey"
)

if api_key_input:
    st.session_state.gemini_api_key = api_key_input
    try:
        genai.configure(api_key=st.session_state.gemini_api_key)
        st.sidebar.success("Connected")
    except Exception:
        st.sidebar.error("Invalid key")
else:
    st.sidebar.warning("Add key for AI ideas")

# ==================== DASHBOARD ====================
if page == "Dashboard":
    st.title("ViralForge")
    st.markdown("### Build a viral page. Secure brand deals & ad revenue.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Followers", f"{st.session_state.followers:,}", "+127")
    col2.metric("Engagement", f"{st.session_state.engagement_rate}%", "+0.3%")
    col3.metric("Est. Monthly", "$1,840", "+$320")
    col4.metric("Active Deals", "3", "+1")

    st.markdown("### Growth Trend")
    dates = pd.date_range(end=datetime.today(), periods=30)
    growth = [st.session_state.followers - random.randint(10, 80) * (30-i) for i in range(30)]
    df = pd.DataFrame({"Date": dates, "Followers": growth})
    st.line_chart(df.set_index("Date"), height=320)

    st.markdown("### Today’s Focus")
    st.info("Post 1 high-hook video · Reply to comments in the first hour · Pitch 1 micro-brand")

# ==================== CONTENT IDEA GENERATOR ====================
elif page == "Content Idea Generator":
    st.title("Content Idea Generator")
    st.caption("Powered by Gemini")

    if not st.session_state.gemini_api_key:
        st.warning("Add your Gemini API key in the sidebar to generate ideas.")
        st.stop()

    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Niche", placeholder="e.g. Personal finance for Gen Z")
        platform = st.selectbox("Platform", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X"])
    with col2:
        style = st.selectbox("Style", ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes"])
        num_ideas = st.slider("Number of ideas", 3, 10, 5)

    if st.button("Generate Ideas", type="primary") and niche:
        with st.spinner("Forging ideas..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"""
                Generate {num_ideas} highly scroll-stopping content ideas for {platform} in the niche: "{niche}".
                Style: {style}.
                
                Each idea must have a strong hook in the first 1-3 seconds.
                Make them specific, emotional or valuable, and optimized for {platform}.
                Keep each idea to 1-2 short sentences.
                
                Format as a clean numbered list only.
                """
                response = model.generate_content(prompt)
                ideas_text = response.text.strip()

                st.success("Ideas ready")
                st.markdown(ideas_text)

                lines = [line.strip() for line in ideas_text.split("\n") if line.strip() and any(c.isdigit() for c in line[:3])]
                for i, line in enumerate(lines[:num_ideas]):
                    idea_clean = line.split(".", 1)[-1].strip() if "." in line else line
                    if st.button(f"Save Idea {i+1}", key=f"save_{i}"):
                        st.session_state.posts.append({
                            "idea": idea_clean,
                            "platform": platform,
                            "status": "Idea",
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success(f"Saved idea {i+1}")

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Check your API key or try again later (free tier limits apply).")

# ==================== POST PLANNER ====================
elif page == "Post Planner":
    st.title("Post Planner")

    with st.form("new_post"):
        st.subheader("Add Post")
        idea = st.text_area("Idea / Caption")
        platform = st.selectbox("Platform", ["TikTok", "Instagram", "YouTube", "LinkedIn"])
        scheduled = st.date_input("Date", value=datetime.today() + timedelta(days=1))
        status = st.selectbox("Status", ["Idea", "Scripted", "Filmed", "Posted", "Performing"])
        if st.form_submit_button("Add to Pipeline", type="primary") and idea:
            st.session_state.posts.append({
                "idea": idea,
                "platform": platform,
                "status": status,
                "date": scheduled.strftime("%Y-%m-%d")
            })
            st.success("Added")

    if st.session_state.posts:
        st.subheader("Pipeline")
        df = pd.DataFrame(st.session_state.posts)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No posts yet. Generate ideas or add one above.")

# ==================== ANALYTICS ====================
elif page == "Analytics Tracker":
    st.title("Analytics Tracker")

    st.subheader("Update Metrics")
    c1, c2 = st.columns(2)
    with c1:
        new_followers = st.number_input("Followers", value=st.session_state.followers, step=100)
    with c2:
        new_er = st.number_input("Engagement Rate %", value=st.session_state.engagement_rate, step=0.1, format="%.1f")

    if st.button("Save Metrics", type="primary"):
        st.session_state.followers = new_followers
        st.session_state.engagement_rate = new_er
        st.success("Updated")
        st.rerun()

    score = min(100, (st.session_state.followers / 100) + (st.session_state.engagement_rate * 8))
    st.markdown("### Brand Deal Readiness")
    st.progress(score / 100)
    st.write(f"**{score:.0f}/100**")

    if score < 40:
        st.warning("Focus on consistency and engagement first.")
    elif score < 70:
        st.info("Start building a simple media kit and pitch micro-brands.")
    else:
        st.success("You’re in brand-deal range. Start pitching.")

# ==================== BRAND PITCH ====================
elif page == "Brand Deal Pitch":
    st.title("Brand Deal Pitch")

    brand = st.text_input("Brand Name")
    your_niche = st.text_input("Your Niche")
    followers = st.number_input("Followers", value=st.session_state.followers)
    engagement = st.number_input("Engagement %", value=st.session_state.engagement_rate)

    if st.button("Generate Pitch", type="primary") and brand:
        pitch = f"""Subject: Collaboration Idea — {brand} x ViralForge Creator

Hi {brand} team,

I run a focused page in the {your_niche} space with {followers:,} engaged followers and a {engagement}% engagement rate.

I’d love to explore a simple collaboration that delivers real value to both audiences.

Open to a quick chat this week?

Best,
[Your Name]
[Your Handle]
"""
        st.text_area("Pitch", pitch, height=280)
        st.download_button("Download", pitch, file_name=f"pitch_{brand}.txt")

# ==================== GROWTH PLAYBOOK ====================
elif page == "Growth Playbook":
    st.title("Growth Playbook")

    st.markdown("""
    **Core rules that actually move the needle**

    1. Hook in the first 1–3 seconds  
    2. Post consistently (5–7x per week)  
    3. Reply to comments in the first hour  
    4. Mix trending audio with your unique angle  
    5. Publicly document results (screenshots of growth or revenue)  
    6. Build a one-page media kit early  
    7. Pitch micro-brands first, then use those wins
    """)

    st.subheader("Simple Weekly Rhythm")
    schedule = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Focus": ["Educational", "Story", "Trend", "Tips", "Behind-the-scenes", "Results", "Engagement"]
    })
    st.table(schedule)

st.sidebar.markdown("---")
st.sidebar.caption("ViralForge · Build once. Scale forever.")
