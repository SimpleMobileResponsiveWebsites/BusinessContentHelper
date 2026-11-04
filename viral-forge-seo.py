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

st.set_page_config(page_title="Keyword Report Prompt Generator", layout="wide")
st.title("Keyword Research Report Prompt Generator")
st.caption("Fill in your details, generate a prompt, then paste it into any AI to get a Google Keyword Planner–style report.")

# ====================== TABS ======================
tab1, tab2 = st.tabs(["Main Inputs", "Advanced Context"])

# ====================== MAIN INPUTS ======================
with tab1:
    st.subheader("Core Details")

    business_name = st.text_input(
        "Business / Brand Name",
        value=settings.get("business_name", ""),
        placeholder="e.g. MoneyMind GenZ",
        key="business_name"
    )

    niche = st.text_input(
        "Niche",
        value=settings.get("niche", ""),
        placeholder="e.g. Personal finance for Gen Z",
        key="niche"
    )

    description = st.text_area(
        "Business / Product / Service Description",
        value=settings.get("description", ""),
        placeholder="What do you sell or offer? Who is it for?",
        height=120,
        key="description"
    )

    col1, col2 = st.columns(2)
    with col1:
        keywords = st.text_area(
            "Seed Keywords (comma or line separated)",
            value=settings.get("keywords", ""),
            placeholder="budgeting tips, saving money, side hustles for students",
            height=100,
            key="keywords"
        )
    with col2:
        hashtags = st.text_area(
            "Hashtags (optional)",
            value=settings.get("hashtags", ""),
            placeholder="#genzmoney #budgeting #personalfinance",
            height=100,
            key="hashtags"
        )

    col3, col4 = st.columns(2)
    with col3:
        style_options = ["Educational", "Entertaining", "Storytelling", "Hot Take", "Behind-the-Scenes", "Tutorial", "Motivational", "Controversial", "Informational", "Commercial"]
        style_default = settings.get("style", style_options[0])
        style_index = style_options.index(style_default) if style_default in style_options else 0
        style = st.selectbox("Content / Brand Style", style_options, index=style_index, key="style")

    with col4:
        platform_options = ["Google Search", "YouTube", "TikTok", "Instagram", "LinkedIn", "Multi-platform", "Amazon", "E-commerce"]
        platform_default = settings.get("platform", platform_options[0])
        platform_index = platform_options.index(platform_default) if platform_default in platform_options else 0
        platform = st.selectbox("Primary Platform", platform_options, index=platform_index, key="platform")

    col5, col6 = st.columns(2)
    with col5:
        audience = st.text_input(
            "Target Audience",
            value=settings.get("audience", ""),
            placeholder="e.g. 18-24 year olds interested in personal finance",
            key="audience"
        )
    with col6:
        tone_options = ["Casual", "Professional", "Funny", "Serious", "Inspirational", "Sarcastic", "Empathetic", "Authoritative", "Friendly"]
        tone_default = settings.get("tone", tone_options[0])
        tone_index = tone_options.index(tone_default) if tone_default in tone_options else 0
        tone = st.selectbox("Tone of Voice", tone_options, index=tone_index, key="tone")

    cta = st.text_input(
        "Primary Call-to-Action",
        value=settings.get("cta", ""),
        placeholder="e.g. Sign up for free guide, Shop now, Book a call",
        key="cta"
    )

# ====================== ADVANCED CONTEXT ======================
with tab2:
    st.subheader("Extra Context (improves report quality)")

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input(
            "Target Location / Market",
            value=settings.get("location", "United States"),
            placeholder="e.g. United States, UK, Global",
            key="location"
        )
        language = st.text_input(
            "Language",
            value=settings.get("language", "English"),
            key="language"
        )
    with col2:
        goal_options = ["SEO Traffic", "Paid Ads (Google/Meta)", "Content Ideas", "Product Research", "Competitor Analysis", "All of the above"]
        goal = st.selectbox("Main Goal", goal_options, index=0, key="goal")
        competitors = st.text_input(
            "Competitors or Inspiration Brands",
            value=settings.get("competitors", ""),
            placeholder="e.g. NerdWallet, Investopedia, specific accounts",
            key="competitors"
        )

    extra_notes = st.text_area(
        "Extra Notes / Specific Instructions",
        value=settings.get("extra_notes", ""),
        height=100,
        placeholder="Any constraints, products to highlight, keywords to avoid, etc.",
        key="extra_notes"
    )

# ====================== GENERATE PROMPT ======================
st.divider()

if st.button("Generate Keyword Report Prompt", type="primary", use_container_width=True):
    # Build the prompt
    prompt = f"""You are an expert SEO and PPC keyword research specialist. Create a comprehensive keyword research report in the style of a Google Keyword Planner / Google Ads Keyword Planner export for the following business.

BUSINESS DETAILS:
- Business / Brand Name: {business_name or "Not provided"}
- Niche: {niche or "Not provided"}
- Description: {description or "Not provided"}
- Seed Keywords: {keywords or "None provided — generate relevant ones"}
- Hashtags (for social context): {hashtags or "None"}
- Style: {style}
- Primary Platform: {platform}
- Target Audience: {audience or "Not specified"}
- Tone of Voice: {tone}
- Primary Call-to-Action: {cta or "Not specified"}
- Target Location / Market: {location}
- Language: {language}
- Main Goal: {goal}
- Competitors / Inspiration: {competitors or "None provided"}
- Extra Notes: {extra_notes or "None"}

REPORT REQUIREMENTS:
Produce a structured keyword research report with the following sections:

1. **Executive Summary** (3–5 sentences on keyword opportunity)
2. **Keyword Themes / Clusters** (group related keywords)
3. **Main Keyword Table** — Format as a clean markdown table with these columns:
   - Keyword
   - Intent (Informational / Commercial / Transactional / Navigational)
   - Estimated Monthly Search Volume (realistic range based on niche, e.g. 1K–10K, 10K–100K, or Low/Medium/High)
   - Competition Level (Low / Medium / High)
   - Suggested CPC Range (Low / Medium / High or approximate $ range if reasonable)
   - Difficulty (1–10 or Easy/Medium/Hard)
   - Notes / Opportunity
4. **Long-tail Keyword Opportunities** (separate table or list)
5. **Question-based Keywords** (People Also Ask style)
6. **Negative Keywords** (recommended to exclude)
7. **Content / Ad Angles** that match the tone of voice and style
8. **Priority Keywords** (top 10–15 recommended to focus on first)

Important instructions:
- Use realistic, plausible search volume and competition estimates based on your knowledge of the niche and market. Clearly label them as estimates.
- Focus on keywords that align with the described business, audience, and CTA.
- Include a mix of head terms and long-tail keywords.
- If seed keywords were provided, expand significantly on them.
- Organize the output cleanly with headers, tables, and bullet points so it is easy to scan and export.
- Tailor suggestions to the primary platform and goal where relevant.

Generate the full report now."""

    st.success("Prompt generated! Copy the text below and paste it into ChatGPT, Claude, Grok, or any other AI.")
    st.text_area("Copy this prompt", value=prompt, height=400, key="generated_prompt")

    # Auto-save current settings when generating
    data = {
        "business_name": business_name,
        "niche": niche,
        "description": description,
        "keywords": keywords,
        "hashtags": hashtags,
        "style": style,
        "platform": platform,
        "audience": audience,
        "tone": tone,
        "cta": cta,
        "location": location,
        "language": language,
        "goal": goal,
        "competitors": competitors,
        "extra_notes": extra_notes
    }
    save_settings(data)

# Save button (optional manual save)
if st.button("Save Settings Only"):
    data = {
        "business_name": business_name,
        "niche": niche,
        "description": description,
        "keywords": keywords,
        "hashtags": hashtags,
        "style": style,
        "platform": platform,
        "audience": audience,
        "tone": tone,
        "cta": cta,
        "location": location,
        "language": language,
        "goal": goal,
        "competitors": competitors,
        "extra_notes": extra_notes
    }
    save_settings(data)
    st.success("Settings saved!")

with st.expander("Currently saved settings"):
    st.json(load_settings())
