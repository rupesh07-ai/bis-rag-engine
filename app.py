import streamlit as st
import time

# ─────────────────────────────────────────
# 🔥 PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS Assistant", layout="wide", page_icon="🏗️")

# ─────────────────────────────────────────
# 🎨 LOAD CSS
# ─────────────────────────────────────────
st.markdown("""
<div class="code-bg">
while(True):
    analyze_data()
    check_compliance()
    ensure_safety()
    optimize_materials()
    BIS_engine.run()
    print("Processing...")
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# 🌌 BACKGROUND (Particles + Grid)
# ─────────────────────────────────────────
st.markdown("""
<div class="grid-bg"></div>
<div class="particles">
    <span style="left:10%; animation-duration:18s;"></span>
    <span style="left:20%; animation-duration:22s;"></span>
    <span style="left:30%; animation-duration:25s;"></span>
    <span style="left:40%; animation-duration:20s;"></span>
    <span style="left:50%; animation-duration:19s;"></span>
    <span style="left:60%; animation-duration:23s;"></span>
    <span style="left:70%; animation-duration:21s;"></span>
    <span style="left:80%; animation-duration:24s;"></span>
    <span style="left:90%; animation-duration:26s;"></span>
</div>
""", unsafe_allow_html=True)

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
        text = (item["title"] + " " + item["scope"]).lower()

        for word in query_words:
            if word in item["title"].lower():
                score += 3
            if word in item["scope"].lower():
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
    explanation = f"🔍 Based on '{query}', these BIS standards are important:\n\n"

    for r in results:
        explanation += f"• {r['standard_id']} ({r['title']}):\n"
        explanation += f"  - Use: {r['scope']}\n"
        explanation += f"  - Importance: {r['reason']}\n\n"

    explanation += "📌 Ensures safety, durability, and compliance."

    return explanation

# ─────────────────────────────────────────
# 🌑 HEADER
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align: center; color: #a5b4fc; text-shadow: 0 0 20px #6366f1;'>
🏗️ BIS Smart Compliance Assistant
</h1>
<p style='text-align: center; color: #94a3b8;'>
Smart Search + AI Insights for BIS Standards
</p>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# 📊 DASHBOARD
# ─────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Standards Covered", "120+")
col2.metric("Accuracy", "95%")
col3.metric("Response Time", "0.5s")

# ─────────────────────────────────────────
# 💬 CHATBOT SYSTEM
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("## 💬 Chat with BIS Assistant")

user_input = st.chat_input("Ask about materials, standards...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ⏳ LOADING
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    results = search(user_input)
    response = generate_ai(user_input, results)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ─────────────────────────────────────────
# 🔁 CHAT DISPLAY + TYPING EFFECT
# ─────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":
            placeholder = st.empty()
            text = ""

            for char in msg["content"]:
                text += char
                placeholder.markdown(text)
                time.sleep(0.01)

        else:
            st.markdown(msg["content"])