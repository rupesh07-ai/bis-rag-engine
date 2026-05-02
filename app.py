import streamlit as st
import os

# ─────────────────────────────────────────
# 🔥 PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS AI Assistant", layout="wide", page_icon="🏗️")

# ─────────────────────────────────────────
# 🎨 LOAD CSS
# ─────────────────────────────────────────
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ─────────────────────────────────────────
# 🔍 SIMPLE SEARCH
# ─────────────────────────────────────────
def search(query):
    data = [
        {
            "standard_id": "IS 456",
            "title": "Plain and Reinforced Concrete Code",
            "scope": "Code of practice for reinforced concrete",
            "reason": "Used in cement and building construction"
        },
        {
            "standard_id": "IS 1786",
            "title": "High Strength Deformed Steel Bars",
            "scope": "Steel bars for reinforcement",
            "reason": "Used in RCC structures"
        },
        {
            "standard_id": "IS 269",
            "title": "Ordinary Portland Cement",
            "scope": "Specification for OPC cement",
            "reason": "Used in building construction"
        }
    ]

    query = query.lower()
    results = []

    for item in data:
        text = (item["title"] + item["scope"]).lower()
        if query in text:
            results.append(item)

    return results if results else data

# ─────────────────────────────────────────
# 🤖 FREE AI (NO API)
# ─────────────────────────────────────────
def generate_ai(query, results):

    if not results:
        return "No relevant standards found."

    explanation = f"🔍 Based on your input '{query}', the following BIS standards are important:\n\n"

    for r in results:
        explanation += f"• {r['standard_id']} ({r['title']}):\n"
        explanation += f"  - Used for: {r['scope']}\n"
        explanation += f"  - Importance: {r['reason']}\n\n"

    explanation += "📌 These standards ensure safety, strength, and quality in construction materials and structures."

    return explanation

# ─────────────────────────────────────────
# 🔥 UI
# ─────────────────────────────────────────
st.title("🏗️ AI-Powered BIS Compliance Assistant")
st.caption("Free AI Version (No API Required)")

st.divider()

query = st.text_input("Enter product description:")

if st.button("🚀 Get Recommendations"):

    if not query:
        st.warning("Please enter something")

    else:
        results = search(query)

        # 🔹 SHOW RESULTS
        for r in results:
            st.markdown(f"""
            <div class="card">
                <h4>{r['standard_id']} - {r['title']}</h4>
                <p><b>Scope:</b> {r['scope']}</p>
                <p><b>Why Relevant:</b> {r['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 🔹 AI ANALYSIS (FREE)
        st.subheader("🤖 AI Expert Analysis")

        answer = generate_ai(query, results)

        st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)