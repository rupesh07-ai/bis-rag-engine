import streamlit as st
from query import search
import os
import time
import google.generativeai as genai 

# 🔥 Gemini API key
genai.configure(api_key="AIzaSyDHm0l2nMItkGij99jWf5Fq_r8FcLi7Ry0")  

# 🔥 Page config
st.set_page_config(page_title="BIS AI", layout="wide")

# 🔥 Inline CSS
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 🔥 Auto index
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

# 🤖 Gemini AI function
def generate_answer(query, context):
    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        User query: {query}
        Relevant BIS standards: {context}

        Explain in simple language why these standards are relevant.
        Keep it short and clear.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return "⚠️ AI explanation not available"

# 🔥 Title
st.title("🏗️ BIS Standard Recommendation System")

# 🔍 Input
query = st.text_input("Enter product description:")

# 🔘 Button
if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter a query first")

    else:
        # 🔥 Loading animation
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

        results = search(query)

        progress.empty()
        status.success("🚀 Results ready!")

        if len(results) == 0:
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

            st.subheader("🤖 AI Explanation")
            st.write(ai_answer)