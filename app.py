import streamlit as st
import time

# ─────────────────────────────────────────
# 🔥 PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(page_title="BIS Assistant", layout="wide")

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
# 📌 SIDEBAR
# ─────────────────────────────────────────
st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "💬 Chat",
    "📊 Dashboard"
])

# ─────────────────────────────────────────
# 🔍 SMART SEARCH
# ─────────────────────────────────────────
def search(query):
    data = [
        {"standard_id": "IS 456", "title": "Concrete Code", "scope": "Reinforced concrete", "reason": "Used in construction"},
        {"standard_id": "IS 1786", "title": "Steel Bars", "scope": "Reinforcement steel", "reason": "Used in RCC"},
        {"standard_id": "IS 269", "title": "Cement", "scope": "OPC cement", "reason": "Used in buildings"}
    ]

    results = []
    for item in data:
        if query.lower() in (item["title"] + item["scope"]).lower():
            results.append(item)

    return results if results else data

# ─────────────────────────────────────────
# 🤖 AI (FAKE)
# ─────────────────────────────────────────
def generate_ai(query, results):
    text = f"🔍 Based on '{query}', relevant BIS standards:\n\n"
    for r in results:
        text += f"• {r['standard_id']} - {r['title']} → {r['reason']}\n"
    return text

# ─────────────────────────────────────────
# 🏠 HOME
# ─────────────────────────────────────────
if page == "🏠 Home":

    st.markdown("""
    <div class="fade-in">
    <h1 style='text-align:center;'>🏗️ BIS Smart Compliance Assistant</h1>
    <p style='text-align:center;'>Smart Search + AI Insights</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🚀 What this tool does")
    st.write("Find BIS standards quickly using smart search and AI insights.")

# ─────────────────────────────────────────
# 💬 CHAT
# ─────────────────────────────────────────
if page == "💬 Chat":

    st.markdown("## 💬 Chat with BIS Assistant")
    # 🔎 SEARCH BAR (ADD THIS)
st.markdown("### 🔍 **Quick Search (Type material name)**")

query = st.text_input("Enter material (e.g. cement, steel)")

if st.button("Search"):
    results = search(query)

    for r in results:
        st.markdown(f"""
        <div class="card">
            <h4>{r['standard_id']} - {r['title']}</h4>
            <p><b>Use:</b> {r['scope']}</p>
            <p><b>Why:</b> {r['reason']}</p>
        </div>
        """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask about materials...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # loading
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.005)
            progress.progress(i+1)

        results = search(user_input)
        response = generate_ai(user_input, results)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                placeholder = st.empty()
                text = ""
                for char in msg["content"]:
                    text += char
                    placeholder.markdown(text)
                    time.sleep(0.005)
            else:
                st.markdown(msg["content"])

# ─────────────────────────────────────────
# 📊 DASHBOARD
# ─────────────────────────────────────────
if page == "📊 Dashboard":

    st.markdown("## 📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card"><h2>120+</h2><p>Standards</p></div>', unsafe_allow_html=True)
    col2.markdown('<div class="card"><h2>95%</h2><p>Accuracy</p></div>', unsafe_allow_html=True)
    col3.markdown('<div class="card"><h2>0.5s</h2><p>Speed</p></div>', unsafe_allow_html=True)