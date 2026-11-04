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

settings = load_settings()

st.title("Content Creator Idea Helper")

# Basic info
business_name = st.text_input(
    "Business / Brand Name",
    value=settings.get("business_name", ""),
    placeholder="e.g. MoneyMind GenZ"
)

niche = st.text_input(
    "Niche",
    value=settings.get("niche", ""),
    placeholder="e.g. Personal finance for Gen Z"
)

description = st.text_area(
    "Description",
    value=settings.get("description", ""),
    placeholder="Describe the content idea, product, service, or what you want to talk about...",
    height=100
)

keywords = st.text_input(
    "Keywords / Hashtags",
    value=settings.get("keywords", ""),
    placeholder="e.g. #budgeting #genzmoney #sidehustle"
)

# Style + Platform
col1, col2 = st.columns(2)

with col1:
    style_options = ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes", "Tutorial", "Motivational", "Controversial"]
    style_default = settings.get("style", style_options[0])
    style_index = style_options.index(style_default) if style_default in style_options else 0
    style = st.selectbox("Style", style_options, index=style_index)

with col2:
    platform_options = ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X", "Instagram Carousel", "YouTube Long-form"]
    platform_default = settings.get("platform", platform_options[0])
    platform_index = platform_options.index(platform_default) if platform_default in platform_options else 0
    platform = st.selectbox("Platform", platform_options, index=platform_index)

# Extra useful fields
col3, col4 = st.columns(2)

with col3:
    audience = st.text_input(
        "Target Audience",
        value=settings.get("audience", ""),
        placeholder="e.g. 18-24 year olds starting their first job"
    )

with col4:
    tone_options = ["Casual", "Professional", "Funny", "Serious", "Inspirational", "Sarcastic", "Empathetic"]
    tone_default = settings.get("tone", tone_options[0])
    tone_index = tone_options.index(tone_default) if tone_default in tone_options else 0
    tone = st.selectbox("Tone of Voice", tone_options, index=tone_index)

cta = st.text_input(
    "Call-to-Action (optional)",
    value=settings.get("cta", ""),
    placeholder="e.g. Follow for more tips / Comment 'YES' if you want the free guide"
)

# Save button
if st.button("Save Settings", type="primary"):
    data = {
        "business_name": business_name,
        "niche": niche,
        "description": description,
        "keywords": keywords,
        "style": style,
        "platform": platform,
        "audience": audience,
        "tone": tone,
        "cta": cta
    }
    save_settings(data)
    st.success("Settings saved!")

# Show current saved settings
with st.expander("Currently saved settings"):
    st.json(load_settings())
