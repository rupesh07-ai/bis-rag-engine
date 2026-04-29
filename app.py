import streamlit as st
from query import search
import os
import time
import google.generativeai as genai

# 🔐 Load API key
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# 🔥 Page config
st.set_page_config(page_title="BIS AI", layout="wide")

# 🎨 UI
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

# 🧠 Ensure FAISS index
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

# 🤖 AI FUNCTION (FINAL STRONG)
def generate_answer(query, context):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ API KEY NOT FOUND"

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are a civil engineering expert.

        User Query: {query}

        BIS Standards:
        {context}

        Explain in PROFESSIONAL English:
        - Why these standards are relevant
        - Real-world usage
        - Importance in safety and compliance

        Do NOT repeat the query.
        Do NOT use Hinglish.
        Give a clean and technical explanation.
        """

        response = model.generate_content(prompt)

        if not response.text:
            return "❌ EMPTY RESPONSE"

        return response.text.strip()

    except Exception as e:
        return f"❌ ERROR: {str(e)}"

# 🔥 Title
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("Get BIS standards + AI explanation")

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
        st.warning("Please enter a query")

    else:
        # 🧠 Clean query
        clean_query = query.replace("ka use", "use").replace("me", "in construction")

        # ⏳ Loading
        status = st.empty()
        progress = st.progress(0)

        for i in range(1, 101):
            progress.progress(i)
            time.sleep(0.01)

        results = search(query)

        progress.empty()
        status.success("Results ready!")

        if not results:
            st.warning("No results found")

        else:
            # 📊 Show top 3
            for r in results[:3]:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)

            # 🧠 Better context
            context = "\n".join([
                f"{r['standard_id']} - {r['title']}: {r['scope']}"
                for r in results[:3]
            ])

            # 🤖 AI
            ai_answer = generate_answer(clean_query, context)

            # 🔁 fallback
            if "❌" in ai_answer:
                ai_answer = f"These standards ensure quality, safety and compliance for {clean_query}."

            st.subheader("🤖 AI Explanation")
            st.write(ai_answer)