import streamlit as st

# ─────────────────────────────────────────
# 🔥 PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS Assistant", layout="wide", page_icon="🏗️")

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
# 🔍 SMART SEARCH
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

    query_words = query.lower().split()
    scored_results = []

    for item in data:
        score = 0
        title = item["title"].lower()
        scope = item["scope"].lower()
        text = title + " " + scope

        for word in query_words:
            if word in title:
                score += 3
            if word in scope:
                score += 2
            if word in text:
                score += 1

        if score > 0:
            scored_results.append((score, item))

    scored_results.sort(reverse=True, key=lambda x: x[0])
    results = [item for score, item in scored_results]

    return results if results else data

# ─────────────────────────────────────────
# 🤖 FREE AI
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
# 🌑 HEADER (DARK MODE STYLE)
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align: center; color: #a5b4fc;'>
🏗️ BIS Smart Compliance Assistant
</h1>
<p style='text-align: center; color: #94a3b8;'>
Find the right BIS standards instantly with smart search + AI insights
</p>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# 🔎 INPUT
# ─────────────────────────────────────────
st.markdown("#### 🔎 Enter product / material name")

query = st.text_input("e.g. cement, steel, concrete")

# ─────────────────────────────────────────
# 🔘 CENTER BUTTON
# ─────────────────────────────────────────
col1, col2, col3 = st.columns([1,2,1])

with col2:
    clicked = st.button("🚀 Get Recommendations")

# ─────────────────────────────────────────
# 🔥 MAIN ACTION
# ─────────────────────────────────────────
if clicked:

    if not query:
        st.warning("⚠️ Please enter something")

    else:
        results = search(query)

        # 📊 RESULTS
        st.markdown("## 📊 Recommended Standards")

        for r in results:
            st.markdown(f"""
            <div class="card">
                <h4>{r['standard_id']} - {r['title']}</h4>
                <p><b>Scope:</b> {r['scope']}</p>
                <p><b>Why Relevant:</b> {r['reason']}</p>
            </div>
            """, unsafe_allow_html=True)

        # 🤖 AI
        st.markdown("## 🤖 AI Insights")

        answer = generate_ai(query, results)

        st.markdown(f'<div class="ai-box">{answer}</div>', unsafe_allow_html=True)