import streamlit as st
from query import search

st.set_page_config(page_title="BIS AI System", layout="wide")

st.title("🏗️ BIS Standard Recommendation System")
st.markdown("### 🔍 Find relevant BIS standards instantly using AI")

query = st.text_input("Enter product description:")

if st.button("🚀 Get Recommendations"):
    results = search(query)

    for r in results:
        st.markdown(f"""
        <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; margin-bottom:10px;">
        <h4>{r['standard_id']} - {r['title']}</h4>
        <p><b>Scope:</b> {r['scope']}</p>
        <p><b>Why Relevant:</b> {r['reason']}</p>
        </div>
        """, unsafe_allow_html=True)