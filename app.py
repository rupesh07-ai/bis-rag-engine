import streamlit as st
import time

st.set_page_config(page_title="BIS Assistant", layout="wide")

# ─────────────────────────────────────────
# 🔍 DATA
# ─────────────────────────────────────────
data = [
    {"standard_id": "IS 456", "title": "Concrete Code", "scope": "Reinforced concrete", "reason": "Used in construction"},
    {"standard_id": "IS 1786", "title": "Steel Bars", "scope": "Reinforcement steel", "reason": "Used in RCC"},
    {"standard_id": "IS 269", "title": "Cement", "scope": "OPC cement", "reason": "Used in buildings"}
]

# ─────────────────────────────────────────
# 🔍 SEARCH
# ─────────────────────────────────────────
def search(query):
    results = []
    for item in data:
        if query.lower() in (item["title"] + item["scope"]).lower():
            results.append(item)
    return results if results else data

# ─────────────────────────────────────────
# 🤖 AI (DETAILED VERSION)
# ─────────────────────────────────────────
def generate_ai(query, results):

    text = f"""
## 🔍 AI Analysis for **{query}**

Based on your query, here are the most relevant BIS standards and their importance:

"""

    for r in results:
        text += f"""
### 🏗️ {r['standard_id']} – {r['title']}

**📌 Scope:**  
{r['scope']}

**💡 Why Important:**  
{r['reason']}

**⚠️ Real-world Impact:**  
This standard plays a critical role in ensuring structural safety, improving durability, and maintaining quality standards in construction projects. It helps engineers follow proper guidelines and prevents failures.

---
"""

    text += """
## 🚀 Final Insight

Following BIS standards ensures:

- ✔ Structural safety  
- ✔ Long-term durability  
- ✔ Legal compliance  
- ✔ High construction quality  

👉 This makes your project safe, reliable, and industry-compliant.
"""

    return text

# ─────────────────────────────────────────
# UI
# ─────────────────────────────────────────
st.title("🏗️ BIS Smart Compliance Assistant")

st.markdown("## 🔍 Smart Search + AI")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type material (cement, steel...)")

if user_input:

    # user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # loading animation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i+1)

    # search
    results = search(user_input)

    # show results
    st.markdown("### 📊 Recommended Standards")

    for r in results:
        st.markdown(f"""
        <div style="padding:10px; border:1px solid #444; border-radius:10px; margin-bottom:10px;">
        <b>{r['standard_id']} - {r['title']}</b><br>
        {r['scope']}
        </div>
        """, unsafe_allow_html=True)

    # 🤖 AI RESPONSE
    response = generate_ai(user_input, results)

    # 🔥 IMPORTANT — AI answer visible section
    st.markdown("## 🤖 AI Explanation")
    st.markdown(response)

    # chat में भी डालो
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ─────────────────────────────────────────
# CHAT DISPLAY
# ─────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])