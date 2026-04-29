import streamlit as st
from query import search
import os
import time
import google.generativeai as genai

# ─────────────────────────────────────────
# 🔐 API KEY LOADING
# ─────────────────────────────────────────
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    return None

API_KEY = get_api_key()

# ─────────────────────────────────────────
# 🔥 Page Config
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS AI Assistant", layout="wide", page_icon="🏗️")

# ─────────────────────────────────────────
# 🎨 Styling
# ─────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #f0f2f6; }

.card {
    background: white;
    padding: 18px 22px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 4px solid #2563eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.card h4 { color: #1e40af; }

.ai-box {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #93c5fd;
    border-radius: 12px;
    padding: 18px;
    margin-top: 16px;
}

.error-box {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    border-radius: 10px;
    padding: 14px;
    color: #991b1b;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 🧠 FAISS Index Check
# ─────────────────────────────────────────
if not os.path.exists("faiss_index.bin"):
    with st.spinner("Building index..."):
        os.system("python embed.py")

# ─────────────────────────────────────────
# 🤖 AI FUNCTION (FINAL FIXED)
# ─────────────────────────────────────────
def generate_answer(query, context):

    api_key = get_api_key()

    if not api_key:
        return "❌ API KEY NOT FOUND", False

    try:
        genai.configure(api_key=api_key)

        # ✅ FIXED MODEL
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
        except:
            model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
You are a civil engineering expert.

User Query: {query}

BIS Standards:
{context}

Explain:
- Why each standard is relevant
- Real-world usage
- Safety importance

Rules:
- Use clean English
- Mention IS numbers
- No generic answers
- Keep it 4-5 lines
"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.9,
                max_output_tokens=400
            )
        )

        if not response.candidates:
            return "❌ No response from model", False

        text = response.text.strip()

        if not text:
            return "❌ Empty response", False

        return text, True

    except Exception as e:
        return f"❌ API Error: {str(e)}", False

# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ BIS Compliance AI Assistant")
st.caption("Powered by Gemini LLM + FAISS search")

# API key status
if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY missing")
else:
    st.success("API Key Loaded")

st.divider()

query = st.text_input("Enter product description:")

if st.button("🚀 Search"):

    if not query:
        st.warning("Enter something first")

    else:
        with st.spinner("Searching..."):
            results = search(query)

        if not results:
            st.warning("No results found")

        else:
            # Show results
            for r in results[:3]:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

            # Context
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