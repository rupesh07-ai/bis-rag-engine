import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="BIS Assistant", layout="wide")

# 🔥 LOAD CSS
def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()

# ─────────────────────────────────────────
# DATA
# ─────────────────────────────────────────
data = [
    {"standard_id": "IS 456", "title": "Concrete Code", "scope": "Reinforced concrete", "reason": "Used in construction"},
    {"standard_id": "IS 1786", "title": "Steel Bars", "scope": "Reinforcement steel", "reason": "Used in RCC"},
    {"standard_id": "IS 269", "title": "Cement", "scope": "OPC cement", "reason": "Used in buildings"}
]

# ─────────────────────────────────────────
# SCORING SEARCH
# ─────────────────────────────────────────
def score_item(query, item):
    score = 0
    q = query.lower().split()
    text = (item["title"] + " " + item["scope"]).lower()

    for w in q:
        if w in item["title"].lower(): score += 3
        if w in item["scope"].lower(): score += 2
        if w in text: score += 1

    return score

def search(query):
    scored = [(score_item(query, d), d) for d in data]
    scored.sort(reverse=True, key=lambda x: x[0])

    max_score = scored[0][0] if scored else 1

    results = []
    for s, d in scored:
        confidence = int((s / max_score) * 100) if max_score else 0
        results.append({**d, "confidence": confidence})

    return results

# ─────────────────────────────────────────
# AI EXPLANATION
# ─────────────────────────────────────────
def generate_ai(query, results):

    text = f"""
## 🔍 AI Analysis for **{query}**
"""

    for i, r in enumerate(results, start=1):
        text += f"""
### {i}. 🏗️ {r['standard_id']} – {r['title']}
**Scope:** {r['scope']}  
**Why:** {r['reason']}
---
"""

    return text

# ─────────────────────────────────────────
# UI
# ─────────────────────────────────────────
st.title("🏗️ BIS Smart Compliance Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Type material (cement, steel...)")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.003)
        progress.progress(i+1)

    results = search(user_input)

    top = results[0]
    st.markdown(f"### 🥇 Best Match ({top['confidence']}%)")

    st.markdown(f"""
    <div style="border:2px solid gold; padding:15px; border-radius:10px;">
    <b>{top['standard_id']} - {top['title']}</b><br>
    {top['scope']}<br>
    <i>{top['reason']}</i>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Other Results")

    for r in results[1:]:
        st.markdown(f"""
        <div style="padding:10px; border:1px solid #444; border-radius:10px;">
        {r['standard_id']} - {r['title']} ({r['confidence']}%)
        </div>
        """, unsafe_allow_html=True)

    df = pd.DataFrame(results)

    st.markdown("### 📈 Insights")
    st.metric("Results Found", len(results))
    st.metric("Top Confidence", f"{top['confidence']}%")

    st.bar_chart(df["confidence"])

    response = generate_ai(user_input, results)

    st.markdown("## 🤖 AI Explanation")
    st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.download_button(
        "📄 Download Report",
        response,
        file_name="report.txt"
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])