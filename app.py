import streamlit as st
from query import search
import os
import time
import google.generativeai as genai

# ─────────────────────────────────────────
# 🔐 API KEY LOADING — Streamlit-safe
# ─────────────────────────────────────────
def get_api_key():
    # 1️⃣ Streamlit secrets (recommended for Streamlit Cloud)
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    # 2️⃣ Environment variable (local dev)
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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap');

html, body, .stApp {
    background: #f0f2f6;
    font-family: 'IBM Plex Sans', sans-serif;
}
.card {
    background: white;
    padding: 18px 22px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 4px solid #2563eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.card h4 { color: #1e40af; margin-bottom: 6px; }
.ai-box {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #93c5fd;
    border-radius: 12px;
    padding: 18px 22px;
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
    with st.spinner("Building search index..."):
        os.system("python embed.py")

# ─────────────────────────────────────────
# 🤖 AI GENERATION — No fake fallback
# ─────────────────────────────────────────
def generate_answer(query: str, context: str) -> tuple[str, bool]:
    """
    Returns (answer_text, success_bool)
    No silent fallback — real errors shown to user.
    """
    api_key = get_api_key()

    if not api_key:
        return (
            "**API Key Missing!**\n\n"
            "Add `GEMINI_API_KEY` to:\n"
            "- `.streamlit/secrets.toml` → `GEMINI_API_KEY = 'your-key'`\n"
            "- OR as environment variable",
            False
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""You are a senior civil engineering expert specializing in Indian BIS standards.

User Query: {query}

Relevant BIS Standards Found:
{context}

Your Task:
1. Explain which standard applies and WHY it matters for this use case
2. Mention key specification requirements (grade, strength, tolerances)
3. State the safety/compliance importance in Indian construction context
4. Keep it professional, precise, 4-5 lines

Rules:
- Write in clean English only
- No repetition of the query
- No generic filler phrases
- Cite the standard numbers (IS XXXX) when relevant

Answer:"""

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.92,
                max_output_tokens=400,
            )
        )

        # Proper response validation
        if not response.candidates:
            return "Model returned no candidates. Try rephrasing your query.", False

        finish_reason = response.candidates[0].finish_reason
        if finish_reason.name not in ("STOP", "MAX_TOKENS"):
            return f"Generation stopped: {finish_reason.name}. Query may be filtered.", False

        text = response.text.strip()
        if not text:
            return "Empty response received. Please try again.", False

        return text, True

    except genai.types.BlockedPromptException:
        return "Query was blocked by safety filters. Try rephrasing.", False
    except Exception as e:
        return f"API Error: {type(e).__name__}: {str(e)}", False

# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ BIS Compliance AI Assistant")
st.caption("Powered by Gemini 1.5 Flash + FAISS semantic search")

# API key status indicator
if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found. Add it to `.streamlit/secrets.toml`")
else:
    st.success("✅ API Key loaded", icon="🔑")

st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input(
        "🔍 Enter product / material description:",
        placeholder="e.g. cement for RCC construction"
    )

with col2:
    top_k = st.selectbox("Show results:", [3, 5, 10], index=0)

# Example chips
st.markdown("**💡 Try these:**")
examples = ["cement for building construction", "steel bars for reinforcement", "concrete mix for bridges", "clay bricks for walls"]
cols = st.columns(4)
for i, ex in enumerate(examples):
    if cols[i].button(ex, key=f"ex_{i}"):
        query = ex

st.divider()

if st.button("🚀 Search & Analyse", type="primary", disabled=not query):
    with st.spinner("Searching BIS database..."):
        results = search(query)

    if not results:
        st.warning("No matching BIS standards found. Try different keywords.")
    else:
        st.subheader(f"📋 Top {min(top_k, len(results))} Matching Standards")

        for r in results[:top_k]:
            st.markdown(f"""
            <div class="card">
                <h4>📌 {r['standard_id']} — {r['title']}</h4>
                <p><b>Scope:</b> {r['scope']}</p>
                <p><b>Why Relevant:</b> {r['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Build rich context for AI
        context = "\n".join([
            f"- {r['standard_id']} ({r['title']}): {r['scope']}"
            for r in results[:top_k]
        ])

        st.subheader("🤖 AI Expert Analysis")

        with st.spinner("Generating expert explanation..."):
            ai_answer, success = generate_answer(query, context)

        if success:
            st.markdown(f'<div class="ai-box">{ai_answer}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">⚠️ {ai_answer}</div>', unsafe_allow_html=True)