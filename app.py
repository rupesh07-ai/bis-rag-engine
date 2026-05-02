import streamlit as st
import os

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
        st.warning("CSS not loaded")

load_css()

# ─────────────────────────────────────────
# 🔍 TEMP SEARCH FUNCTION (NO FAISS)
# ─────────────────────────────────────────
def search(query):
    return [
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
        }
    ]

# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("Stable Version (FAISS Disabled)")

if not API_KEY:
    st.warning("⚠️ API key optional (AI disabled)")
else:
    st.success("✅ API Key Loaded")

st.divider()

query = st.text_input("Enter product description:")

if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter something")

    else:
        results = search(query)

        # 🔹 SHOW RESULTS
        for r in results:
            st.markdown(f"""
            <div class="card">
                <h4>{r['standard_id']} - {r['title']}</h4>
                <p><b>Scope:</b> {r['scope']}</p>
                <p><b>Why Relevant:</b> {r['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 🔹 AI DISABLED
        st.subheader("🤖 AI Expert Analysis")
        st.success("AI temporarily disabled (app stable now)")