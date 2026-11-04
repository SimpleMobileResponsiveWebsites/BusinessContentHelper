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

# ====================== TABS ======================
tab1, tab2 = st.tabs(["View 1 - Simple", "View 2 - Advanced"])

# ====================== VIEW 1 ======================
with tab1:
    st.subheader("Simple View")

    business_name = st.text_input(
        "Business / Brand Name",
        value=settings.get("business_name", ""),
        placeholder="e.g. MoneyMind GenZ",
        key="v1_business"
    )

    niche = st.text_input(
        "Niche",
        value=settings.get("niche", ""),
        placeholder="e.g. Personal finance for Gen Z",
        key="v1_niche"
    )

    description = st.text_area(
        "Description",
        value=settings.get("description", ""),
        placeholder="Describe the content idea, product, service...",
        height=100,
        key="v1_desc"
    )

    keywords = st.text_input(
        "Keywords / Hashtags",
        value=settings.get("keywords", ""),
        placeholder="e.g. #budgeting #genzmoney",
        key="v1_keywords"
    )

    col1, col2 = st.columns(2)
    with col1:
        style_options = ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes", "Tutorial", "Motivational", "Controversial"]
        style_default = settings.get("style", style_options[0])
        style_index = style_options.index(style_default) if style_default in style_options else 0
        style = st.selectbox("Style", style_options, index=style_index, key="v1_style")

    with col2:
        platform_options = ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X", "Instagram Carousel", "YouTube Long-form"]
        platform_default = settings.get("platform", platform_options[0])
        platform_index = platform_options.index(platform_default) if platform_default in platform_options else 0
        platform = st.selectbox("Platform", platform_options, index=platform_index, key="v1_platform")

    col3, col4 = st.columns(2)
    with col3:
        audience = st.text_input(
            "Target Audience",
            value=settings.get("audience", ""),
            placeholder="e.g. 18-24 year olds",
            key="v1_audience"
        )

    with col4:
        tone_options = ["Casual", "Professional", "Funny", "Serious", "Inspirational", "Sarcastic", "Empathetic"]
        tone_default = settings.get("tone", tone_options[0])
        tone_index = tone_options.index(tone_default) if tone_default in tone_options else 0
        tone = st.selectbox("Tone of Voice", tone_options, index=tone_index, key="v1_tone")

    cta = st.text_input(
        "Call-to-Action (optional)",
        value=settings.get("cta", ""),
        placeholder="e.g. Follow for more tips",
        key="v1_cta"
    )

    if st.button("Save Settings", type="primary", key="v1_save"):
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
        # Preserve any extra fields from View 2
        existing = load_settings()
        existing.update(data)
        save_settings(existing)
        st.success("Settings saved from View 1!")

# ====================== VIEW 2 ======================
with tab2:
    st.subheader("Advanced View")

    # --- Basic ---
    st.markdown("### Basic Info")
    business_name2 = st.text_input("Business / Brand Name", value=settings.get("business_name", ""), key="v2_business")
    niche2 = st.text_input("Niche", value=settings.get("niche", ""), key="v2_niche")
    description2 = st.text_area("Description", value=settings.get("description", ""), height=80, key="v2_desc")
    keywords2 = st.text_input("Keywords / Hashtags", value=settings.get("keywords", ""), key="v2_keywords")

    # --- Strategy ---
    st.markdown("### Strategy")
    col1, col2, col3 = st.columns(3)
    with col1:
        goal_options = ["Awareness", "Engagement", "Leads", "Sales", "Followers", "Authority", "Education"]
        goal = st.selectbox("Goal", goal_options, index=goal_options.index(settings.get("goal", goal_options[0])) if settings.get("goal") in goal_options else 0, key="v2_goal")
    with col2:
        length_options = ["15s", "30s", "60s", "90s", "3-5 min", "Carousel (5-10 slides)", "Long-form"]
        length = st.selectbox("Content Length", length_options, index=length_options.index(settings.get("length", length_options[0])) if settings.get("length") in length_options else 0, key="v2_length")
    with col3:
        frequency_options = ["Daily", "3x/week", "Weekly", "2x/week", "Monthly"]
        frequency = st.selectbox("Posting Frequency", frequency_options, index=frequency_options.index(settings.get("frequency", frequency_options[0])) if settings.get("frequency") in frequency_options else 0, key="v2_freq")

    # --- Audience & Messaging ---
    st.markdown("### Audience & Messaging")
    col4, col5 = st.columns(2)
    with col4:
        audience2 = st.text_input("Target Audience", value=settings.get("audience", ""), key="v2_audience")
        pain_points = st.text_area("Pain Points", value=settings.get("pain_points", ""), height=70, placeholder="What problems does the audience have?", key="v2_pain")
    with col5:
        desired_outcome = st.text_area("Desired Outcome", value=settings.get("desired_outcome", ""), height=70, placeholder="What should the viewer feel or do after?", key="v2_outcome")
        key_message = st.text_input("Key Message / Takeaway", value=settings.get("key_message", ""), key="v2_message")

    hook_style_options = ["Question", "Shocking Stat", "Story", "Stop Scrolling If...", "Bold Claim", "Tutorial Promise"]
    hook_style = st.selectbox("Preferred Hook Style", hook_style_options, index=hook_style_options.index(settings.get("hook_style", hook_style_options[0])) if settings.get("hook_style") in hook_style_options else 0, key="v2_hook")

    # --- Creative Direction ---
    st.markdown("### Creative Direction")
    col6, col7, col8 = st.columns(3)
    with col6:
        style2 = st.selectbox("Style", ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes", "Tutorial", "Motivational", "Controversial"], key="v2_style")
        visual_options = ["Talking Head", "B-roll Heavy", "Screen Recording", "Text-on-Screen", "UGC Style", "AI Generated", "Mix"]
        visual = st.selectbox("Visual Style", visual_options, index=visual_options.index(settings.get("visual", visual_options[0])) if settings.get("visual") in visual_options else 0, key="v2_visual")
    with col7:
        platform2 = st.selectbox("Platform", ["TikTok", "Instagram Reels", "YouTube Shorts", "LinkedIn", "Twitter/X", "Instagram Carousel", "YouTube Long-form"], key="v2_platform")
        music_options = ["Trending Sound", "Calm", "Upbeat", "Dramatic", "No Music", "Original Audio"]
        music = st.selectbox("Music / Vibe", music_options, index=music_options.index(settings.get("music", music_options[0])) if settings.get("music") in music_options else 0, key="v2_music")
    with col8:
        tone2 = st.selectbox("Tone of Voice", ["Casual", "Professional", "Funny", "Serious", "Inspirational", "Sarcastic", "Empathetic"], key="v2_tone")
        talent_options = ["Just Me", "Team", "Voiceover Only", "UGC Creator", "No Face"]
        talent = st.selectbox("On-camera Talent", talent_options, index=talent_options.index(settings.get("talent", talent_options[0])) if settings.get("talent") in talent_options else 0, key="v2_talent")

    # --- Output Preferences ---
    st.markdown("### Output Preferences")
    col9, col10 = st.columns(2)
    with col9:
        num_ideas = st.number_input("Number of Ideas to Generate", min_value=1, max_value=50, value=settings.get("num_ideas", 5), key="v2_num")
        include_script = st.radio("Include Script?", ["Outline only", "Full script", "Hooks + Outline"], index=["Outline only", "Full script", "Hooks + Outline"].index(settings.get("include_script", "Outline only")), key="v2_script")
    with col10:
        cta_type_options = ["Follow", "Comment", "DM", "Link in bio", "Save", "Share", "None"]
        cta_type = st.selectbox("CTA Type", cta_type_options, index=cta_type_options.index(settings.get("cta_type", cta_type_options[0])) if settings.get("cta_type") in cta_type_options else 0, key="v2_cta_type")
        cta2 = st.text_input("Custom CTA text", value=settings.get("cta", ""), key="v2_cta")

    # --- Business Context ---
    st.markdown("### Business Context")
    col11, col12 = st.columns(2)
    with col11:
        product = st.text_input("Product / Offer (if any)", value=settings.get("product", ""), key="v2_product")
        usp = st.text_area("Unique Selling Point", value=settings.get("usp", ""), height=70, key="v2_usp")
    with col12:
        competitors = st.text_input("Competitors / Inspiration accounts", value=settings.get("competitors", ""), key="v2_comp")
        language = st.text_input("Language", value=settings.get("language", "English"), key="v2_lang")

    extra_notes = st.text_area("Extra Notes / Instructions", value=settings.get("extra_notes", ""), height=80, key="v2_notes")

    if st.button("Save Settings", type="primary", key="v2_save"):
        data = {
            "business_name": business_name2,
            "niche": niche2,
            "description": description2,
            "keywords": keywords2,
            "goal": goal,
            "length": length,
            "frequency": frequency,
            "audience": audience2,
            "pain_points": pain_points,
            "desired_outcome": desired_outcome,
            "key_message": key_message,
            "hook_style": hook_style,
            "style": style2,
            "visual": visual,
            "platform": platform2,
            "music": music,
            "tone": tone2,
            "talent": talent,
            "num_ideas": num_ideas,
            "include_script": include_script,
            "cta_type": cta_type,
            "cta": cta2,
            "product": product,
            "usp": usp,
            "competitors": competitors,
            "language": language,
            "extra_notes": extra_notes
        }
        save_settings(data)
        st.success("Settings saved from View 2!")

# Show current settings at the bottom
with st.expander("Currently saved settings"):
    st.json(load_settings())
