import streamlit as st
import requests
import pandas as pd
import json

# ================= CONFIG =================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="wide"
)

# ================= STYLES =================
st.markdown("""
<style>
.card {
    background-color: #f8f9fa;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
    border-left: 5px solid #4f46e5;
}
.badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def check_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        return r.status_code == 200, r.json()
    except:
        return False, {}

def get_recommendations(query, k):
    r = requests.post(
        f"{API_URL}/recommend",
        json={"query": query, "max_results": k},
        timeout=10
    )
    return r.json()

def render_card(a):
    st.markdown(f"""
    <div class="card">
        <h4>{a['name']}</h4>
        <p>{a['description']}</p>
        <span class="badge">⏱ {a['duration']} min</span>
        <span class="badge">🌍 Remote: {a['remote_support']}</span>
        <span class="badge">🧠 Adaptive: {a['adaptive_support']}</span><br><br>
        {''.join([f"<span class='badge'>{t}</span>" for t in a['test_type']])}
        <br><br>
        <a href="{a['url']}" target="_blank">🔗 View on SHL</a>
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN UI =================
st.title("🎯 SHL Assessment Recommendation System")

# -------- Sidebar --------
with st.sidebar:
    st.header("⚙️ System Status")

    ok, data = check_health()
    if ok:
        st.success("API Connected")
        st.metric("Total Assessments", data["total_assessments"])
    else:
        st.error("API Not Reachable")

    st.divider()
    st.info("""
    💡 Tips:
    - Mention role clearly
    - Add skills & experience
    - Specify time limit
    """)

# -------- Query Input --------
query = st.text_area(
    "Enter Job Description or Hiring Requirement",
    height=150,
    placeholder="Example: Hiring a Java developer with strong problem-solving and communication skills."
)

col1, col2 = st.columns(2)
with col1:
    k = st.slider("Number of recommendations", 5, 10, 10)
with col2:
    run = st.button("🎯 Get Recommendations", use_container_width=True)

# -------- Run Recommendation --------
if run:
    if not query.strip():
        st.warning("Please enter a query")
    else:
        with st.spinner("Finding best SHL assessments..."):
            res = get_recommendations(query, k)

        recs = res.get("recommendations", [])

        if not recs:
            st.error("No recommendations returned")
        else:
            # Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Recommendations", len(recs))
            m2.metric("Remote Tests", sum(1 for r in recs if r["remote_support"] == "Yes"))
            m3.metric("Adaptive Tests", sum(1 for r in recs if r["adaptive_support"] == "Yes"))

            st.divider()

            # Cards
            for a in recs:
                render_card(a)

            # Export
            df = pd.DataFrame(recs)
            csv = df.to_csv(index=False)

            st.download_button(
                "⬇️ Download CSV",
                csv,
                "shl_recommendations.csv",
                "text/csv"
            )

# -------- Footer --------
st.divider()
st.caption("SHL Assessment Recommendation System • Built with RAG & Semantic Search")
