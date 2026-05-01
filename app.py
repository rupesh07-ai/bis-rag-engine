import streamlit as st
from query import search
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
# 🎨 LOAD CSS (IMPORTANT FIX)
# ─────────────────────────────────────────
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        st.warning("CSS not loaded")

load_css()

# ─────────────────────────────────────────
# 🧠 INDEX CHECK
# ─────────────────────────────────────────
if not os.path.exists("faiss_index.bin"):
    st.error("❌ Index file missing. Run embed.py locally and push.")
    st.stop()

# ─────────────────────────────────────────
# 🤖 AI FUNCTION (STABLE)
# ─────────────────────────────────────────
def generate_answer(query, context):

    api_key = get_api_key()

    if not api_key:
        return "❌ API KEY NOT FOUND", False

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
You are a civil engineering expert.

User Query: {query}

BIS Standards:
{context}

Explain clearly:
- Why each standard is relevant
- Real-world usage
- Safety importance

Keep it short (4-5 lines)
"""
        )

        text = response.text

        if not text:
            return "❌ Empty response", False

        return text.strip(), True

    except Exception as e:
        return f"❌ ERROR: {str(e)}", False

# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("FAISS + Gemini AI System")

if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY missing")
else:
    st.success("✅ API Key Loaded")

st.divider()

query = st.text_input("Enter product description:")

if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter something")

    else:
        with st.spinner("Searching..."):
            results = search(query)

        if not results:
            st.warning("No results found")

        else:
            # 🔹 SHOW RESULTS
            for r in results[:3]:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

            # 🔹 CONTEXT
            context = "\n".join([
                f"{r['standard_id']} ({r['title']}): {r['scope']}"
                for r in results[:3]
            ])

            st.subheader("🤖 AI Expert Analysis")

            with st.spinner("Generating explanation..."):
                answer, ok = generate_answer(query, context)

            if ok:
                st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-box">{answer}</div>', unsafe_allow_html=True)