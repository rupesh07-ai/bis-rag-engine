import streamlit as st
from query import search
import os
import time

# 🔥 Page config
st.set_page_config(page_title="BIS AI", layout="wide")

# 🔥 Inline CSS (fix white issue everywhere)
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}

/* Card UI */
.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 🔥 Auto create index (first time only)
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

# 🔥 Title
st.title("🏗️ BIS Standard Recommendation System")

# 🔍 Input
query = st.text_input("Enter product description:")

# 🔘 Button
if st.button("🚀 Get Recommendations"):
    
    if not query:
        st.warning("Please enter a query first")
    
    else:
        # 🔥 Premium loading animation
        status = st.empty()
        progress = st.progress(0)

        status.markdown("🔍 Analyzing product description...")

        for i in range(1, 101):
            progress.progress(i)
            time.sleep(0.01)  # smooth animation

            if i == 40:
                status.markdown("⚡ Matching with BIS standards...")
            elif i == 80:
                status.markdown("📊 Generating recommendations...")

        # 🔍 Actual search
        results = search(query)

        progress.empty()
        status.success("🚀 Results ready!")

        # 📊 Show results
        if len(results) == 0:
            st.warning("No results found")
        else:
            for r in results:
                st.markdown(f"""
                <div class="card">
                    <h4>{r['standard_id']} - {r['title']}</h4>
                    <p><b>Scope:</b> {r['scope']}</p>
                    <p><b>Why Relevant:</b> {r['reason']}</p>
                </div>
                """, unsafe_allow_html=True)