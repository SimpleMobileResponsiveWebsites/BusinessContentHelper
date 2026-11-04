import streamlit as st
import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Load previous values
settings = load_settings()

st.title("Content Idea Helper")

# Niche input
niche = st.text_input(
    "Niche",
    value=settings.get("niche", ""),
    placeholder="e.g. Personal finance for Gen Z"
)

# Style + Platform in columns
col1, col2 = st.columns(2)

with col1:
    style_options = ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes"]
    style_index = style_options.index(settings.get("style", style_options[0])) if settings.get("style") in style_options else 0
    style = st.selectbox("Style", style_options, index=style_index)

with col2:
    platform_options = ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X"]
    platform_index = platform_options.index(settings.get("platform", platform_options[0])) if settings.get("platform") in platform_options else 0
    platform = st.selectbox("Platform", platform_options, index=platform_index)

# Save button
if st.button("Save", type="primary"):
    data = {
        "niche": niche,
        "style": style,
        "platform": platform
    }
    save_settings(data)
    st.success("Saved successfully!")

# Optional: show currently saved values
with st.expander("Currently saved settings"):
    st.json(load_settings())
