import streamlit as st
from query import search
import os

# 🔥 Auto create index (only first time)
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

st.set_page_config(page_title="BIS AI", layout="wide")

st.title("🏗️ BIS Standard Recommendation System")

query = st.text_input("Enter product description:")

if query:
    with st.spinner("⚡ Searching..."):
        results = search(query)

    st.success("⚡ Results loaded instantly")

    for r in results:
        st.markdown(f"""
        <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; margin-bottom:10px;">
        <h4>{r['standard_id']} - {r['title']}</h4>
        <p><b>Scope:</b> {r['scope']}</p>
        <p><b>Why Relevant:</b> {r['reason']}</p>
        </div>
        """, unsafe_allow_html=True)