import streamlit as st
from query import search
import os
import time
import google.generativeai as genai

# 🔐 Load API key from env (Streamlit Secrets)
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# 🖼️ Page config
st.set_page_config(page_title="BIS AI", layout="wide")

# 🎨 UI CSS
st.markdown("""
<style>
.stApp { background-color: #f5f7fa; }
.card {
    background: white; padding: 15px; border-radius: 10px;
    margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 🧠 Ensure index exists
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

# 🤖 Gemini function (debug-friendly)
def generate_answer(query, context):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ API KEY NOT FOUND (check Streamlit Secrets)"

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        User query: {query}
        Relevant BIS standards: {context}

        Explain in simple, clear language why these standards are relevant.
        Keep it short (3-5 lines).
        """

        response = model.generate_content(prompt)

        text = getattr(response, "text", None)
        if not text:
            return "❌ EMPTY RESPONSE FROM GEMINI"

        return text

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# 🏗️ Title
st.title("🏗️ BIS Standard Recommendation System")

# 🔍 Input
query = st.text_input("Enter product description:")

# 🚀 Button
if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter a query first")

    else:
        # ⏳ Loading animation
        status = st.empty()
        progress = st.progress(0)

        status.markdown("🔍 Analyzing...")
        for i in range(1, 101):
            progress.progress(i)
            time.sleep(0.01)
            if i == 40:
                status.markdown("⚡ Matching standards...")
            elif i == 80:
                status.markdown("📊 Generating AI explanation...")

        # 🔎 Retrieval
        results = search(query)

        progress.empty()
        status.success("🚀 Results ready!")

        if not results:
            st.warning("No results found")

        else:
            # 📊 Show standards
            for r in results:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

            # 🤖 AI explanation
            context = " ".join([r["title"] for r in results])
            ai_answer = generate_answer(query, context)

            # 🔁 Fallback (demo-safe)
            if "❌" in ai_answer:
                ai_answer = (
                    f"These standards are relevant to '{query}' as they ensure "
                    "quality, safety, and compliance for construction materials."
                )

            st.subheader("🤖 AI Explanation")
            st.write(ai_answer)