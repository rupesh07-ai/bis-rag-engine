import streamlit as st
import os
from google import genai  

# ─────────────────────────────────────────
# 🔐 API KEY
# ─────────────────────────────────────────
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.getenv("GEMINI_API_KEY")

API_KEY = get_api_key()

# ─────────────────────────────────────────
# 🔥 PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS AI Assistant", layout="wide", page_icon="🏗️")

# ─────────────────────────────────────────
# 🎨 LOAD CSS
# ─────────────────────────────────────────
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ─────────────────────────────────────────
# 🔍 SIMPLE SEARCH
# ─────────────────────────────────────────
def search(query):
    data = [
        {
            "standard_id": "IS 456",
            "title": "Plain and Reinforced Concrete Code",
            "scope": "Code of practice for reinforced concrete",
            "reason": "Used in cement and building construction"
        },
        {
            "standard_id": "IS 1786",
            "title": "High Strength Deformed Steel Bars",
            "scope": "Steel bars for reinforcement",
            "reason": "Used in RCC structures"
        },
        {
            "standard_id": "IS 269",
            "title": "Ordinary Portland Cement",
            "scope": "Specification for OPC cement",
            "reason": "Used in building construction"
        }
    ]

    query = query.lower()
    results = []

    for item in data:
        text = (item["title"] + item["scope"]).lower()
        if query in text:
            results.append(item)

    return results if results else data

# ─────────────────────────────────────────
# 🤖 AI FUNCTION (NEW SDK)
# ─────────────────────────────────────────
def generate_ai(query, context):

    if not API_KEY:
        return "❌ API key missing"

    try:
        from google import genai

        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",  # ✅ FIXED
            contents=f"""
User Query: {query}

Relevant BIS Standards:
{context}

Explain clearly:
- Why relevant
- Real-life usage
- Safety importance

Keep it short (4-5 lines).
"""
        )

        return response.text

    except Exception as e:
        return f"❌ ERROR: {str(e)}"
# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("AI Enabled Version 🚀")

st.divider()

query = st.text_input("Enter product description:")

if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter something")

    else:
        results = search(query)

        for r in results:
            st.markdown(f"""
            <div class="card">
                <h4>{r['standard_id']} - {r['title']}</h4>
                <p><b>Scope:</b> {r['scope']}</p>
                <p><b>Why Relevant:</b> {r['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("🤖 AI Expert Analysis")

        context = "\n".join([
            f"{r['standard_id']} ({r['title']}): {r['scope']}"
            for r in results
        ])

        with st.spinner("Generating AI response..."):
            answer = generate_ai(query, context)

        st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)