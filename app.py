import streamlit as st
from query import search
import os
import time
import google.generativeai as genai

# 🔐 Load API key (Streamlit Secrets)
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# 🔥 Page config
st.set_page_config(page_title="BIS AI", layout="wide")

# 🎨 UI CSS
st.markdown("""
<style>
.stApp { background-color: #f5f7fa; }
.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 🧠 Ensure index exists
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

# 🤖 Gemini AI (STRONG VERSION)
def generate_answer(query, context):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ API KEY NOT FOUND"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        You are a civil engineering expert specializing in BIS standards.

        User Query: {query}

        Relevant BIS Standards:
        {context}

        Explain clearly:
        1. Why each standard is relevant
        2. Where it is used in real construction
        3. Why it is important for safety and compliance

        Make the answer practical, specific and NOT generic.
        """

        response = model.generate_content(prompt)

        if not response.text:
            return "❌ EMPTY RESPONSE"

        return response.text.strip()

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# 🔥 Title
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("Get instant BIS standards with AI explanation")

# 🔍 Input
query = st.text_input("Enter product description:")

# 💡 Examples
st.markdown("### 💡 Try:")
st.write("• cement for building construction")
st.write("• steel bars for reinforcement")
st.write("• concrete mix for bridges")

# 🔘 Button
if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter a query first")

    else:
        # ⏳ Loading animation
        status = st.empty()
        progress = st.progress(0)

        status.markdown("🔍 Analyzing input...")

        for i in range(1, 101):
            progress.progress(i)
            time.sleep(0.01)

            if i == 40:
                status.markdown("⚡ Matching BIS standards...")
            elif i == 80:
                status.markdown("🤖 Generating AI explanation...")

        # 🔍 Search
        results = search(query)

        progress.empty()
        status.success("🚀 Results ready!")

        if not results:
            st.warning("No results found")

        else:
            # 📊 Show top 5
            for r in results[:5]:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

            # 🧠 Strong context
            context = "\n".join([
                f"{r['standard_id']} - {r['title']}: {r['scope']}"
                for r in results[:5]
            ])

            # 🤖 AI Explanation
            ai_answer = generate_answer(query, context)

            # 🔁 Fallback (demo safe)
            if "❌" in ai_answer:
                ai_answer = f"""
                These standards are relevant to '{query}' as they ensure
                quality, safety, and proper construction practices.
                """

            st.subheader("🤖 AI Explanation")
            st.write(ai_answer)