import streamlit as st
import json
import time

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS Assistant", layout="wide")

# ─────────────────────────────────────────
# LOAD CSS
# ─────────────────────────────────────────
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ─────────────────────────────────────────
# SAFE DATA LOAD (NO ERROR)
# ─────────────────────────────────────────
def load_data():
    try:
        with open("data/standards.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [
            {"standard_id": "IS 456", "title": "Concrete Code", "scope": "Reinforced concrete", "reason": "Used in construction"},
            {"standard_id": "IS 1786", "title": "Steel Bars", "scope": "Reinforcement steel", "reason": "Used in RCC"},
            {"standard_id": "IS 269", "title": "Cement", "scope": "OPC cement", "reason": "Used in buildings"}
        ]

data = load_data()

# ─────────────────────────────────────────
# SEARCH FUNCTION
# ─────────────────────────────────────────
def search(query):
    results = []
    for item in data:
        if query.lower() in (item["title"] + item["scope"]).lower():
            results.append(item)

    return results if results else data

# ─────────────────────────────────────────
# AI RESPONSE (SAFE)
# ─────────────────────────────────────────
def generate_ai(query, results):
    text = f"🔍 Based on '{query}', these BIS standards are relevant:\n\n"
    for r in results:
        text += f"• {r['standard_id']} ({r['title']}) → {r['reason']}\n"
    text += "\n📌 These ensure safety and compliance."
    return text

# ─────────────────────────────────────────
# UI HEADER
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center;'>🏗️ BIS Smart Compliance Assistant</h1>
<p style='text-align:center;'>Smart Search + AI Insights for BIS Standards</p>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────
# CHAT SYSTEM
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("## 🔍 Smart Search + AI Chat")

user_input = st.chat_input("Type material (cement, steel, road...)")

if user_input:

    # user msg
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # loading
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i + 1)

    # search
    results = search(user_input)

    # 🥇 TOP RESULT
    st.markdown("### 🥇 Best Match")

    top = results[0]
    st.markdown(f"""
    <div class="card" style="border:2px solid gold;">
        <h3>{top['standard_id']} - {top['title']}</h3>
        <p><b>Use:</b> {top['scope']}</p>
        <p><b>Why:</b> {top['reason']}</p>
    </div>
    """, unsafe_allow_html=True)

    # OTHER RESULTS
    st.markdown("### 📊 Other Results")

    for r in results[1:]:
        st.markdown(f"""
        <div class="card">
            <h4>{r['standard_id']} - {r['title']}</h4>
            <p>{r['scope']}</p>
        </div>
        """, unsafe_allow_html=True)

    # AI response
    response = generate_ai(user_input, results)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # SAFE DOWNLOAD
    st.download_button(
        "📄 Download Report",
        response.encode(),
        file_name="report.txt"
    )

# ─────────────────────────────────────────
# CHAT DISPLAY
# ─────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":
            placeholder = st.empty()
            text = ""

            for char in msg["content"]:
                text += char
                placeholder.markdown(text)
                time.sleep(0.003)
        else:
            st.markdown(msg["content"])