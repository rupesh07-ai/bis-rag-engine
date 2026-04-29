import streamlit as st
from query import search
import os

# Auto create index if missing
if not os.path.exists("faiss_index.bin"):
    os.system("python embed.py")

st.title("🏗️ BIS Standard Recommendation System")

query = st.text_input("Enter product description:")

if query:
    st.write("🔍 Searching...")

    results = search(query)

    if len(results) == 0:
        st.warning("No results found")
    else:
        for r in results:
    st.write(f"### {r['standard_id']} - {r['title']}")
    st.write(r["scope"])
    st.write("👉", r["reason"])  