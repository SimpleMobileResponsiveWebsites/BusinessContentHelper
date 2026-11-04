import streamlit as st
from mistralai.client import Mistral
from datetime import datetime

st.set_page_config(page_title="ViralForge", page_icon="⚡", layout="centered")

# ==================== CLEAN CSS ====================
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 780px;
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
    .idea-card {
        background: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 0.8rem;
        color: #0f172a;
    }
    .idea-card small {
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
if "saved_ideas" not in st.session_state:
    st.session_state.saved_ideas = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚡ ViralForge")
    st.caption("Powered by Mistral")
    st.divider()

    api_key = st.text_input(
        "Mistral API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="Paste your Mistral API key"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("Key saved")

    model = st.selectbox(
        "Model",
        [
            "mistral-large-latest",
            "mistral-small-latest",
            "mistral-medium-latest",
            "mistral-large-4",
            "mistral-small-4"
        ],
        index=0
    )

# ==================== MAIN ====================
st.title("ViralForge")
st.markdown("Generate content ideas, save them, and copy to clipboard.")

if not st.session_state.api_key:
    st.info("Add your Mistral API key in the sidebar to get started.")
    st.stop()

# Inputs
niche = st.text_input("Niche", placeholder="e.g. Personal finance for Gen Z")
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style", ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes"])
with col2:
    platform = st.selectbox("Platform", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X"])

num_ideas = st.slider("Number of ideas", 3, 10, 5)

if st.button("Generate Ideas", type="primary", use_container_width=True) and niche:
    with st.spinner("Generating ideas..."):
        try:
            client = Mistral(api_key=st.session_state.api_key)
            prompt = f"""
            Generate {num_ideas} highly scroll-stopping content ideas for {platform} in the niche: "{niche}".
            Style: {style}.
            
            Each idea must have a strong hook in the first 1-3 seconds.
            Make them specific, emotional or valuable, and optimized for {platform}.
            Keep each idea to 1-2 short sentences.
            
            Format as a clean numbered list only.
            """

            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            ideas_text = response.choices[0].message.content.strip()

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

            # Save to session
            st.session_state.saved_ideas.extend(new_ideas)
            st.success(f"Added {len(new_ideas)} ideas")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display saved ideas
if st.session_state.saved_ideas:
    st.markdown("### Saved Ideas")
    
    for i, idea in enumerate(reversed(st.session_state.saved_ideas)):
        with st.container():
            st.markdown(f"""
            <div class="idea-card">
                <strong>{idea['idea']}</strong><br>
                <small>{idea['platform']} · {idea['style']} · {idea['niche']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button
            if st.button("Copy", key=f"copy_{i}"):
                st.write(idea['idea'])  # Fallback display
                st.code(idea['idea'], language=None)
                st.toast("Idea ready to copy (select and copy the text above)")

    # Clear all button
    if st.button("Clear all ideas", type="secondary"):
        st.session_state.saved_ideas = []
        st.rerun()

else:
    st.info("Generate some ideas to see them here.")
