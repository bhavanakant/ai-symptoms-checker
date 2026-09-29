"""
AI-Powered Symptom Checker — Streamlit Application
Powered by Google Gemini 2.5 Flash
"""

import streamlit as st
from analyser import analyse_symptoms
from config import TRIAGE_LEVELS

# ──────────────────────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Symptom Checker",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# Session state initialisation
# ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ──────────────────────────────────────────────────────────────
# Sidebar — API key + history
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your Gemini API key here",
        help="Get your free API key at https://aistudio.google.com/app/apikey",
    )

    st.markdown("---")
    st.markdown("### 📋 Session History")

    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history), start=1):
            triage = entry["triage"]
            icon = TRIAGE_LEVELS.get(triage, {}).get("icon", "⚪")
            short = entry["symptoms"][:40] + ("…" if len(entry["symptoms"]) > 40 else "")
            st.markdown(f"{icon} **{i}.** {short}")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No checks yet. Run your first analysis below.")

    st.markdown("---")
    st.markdown(
        "**Disclaimer:** This tool is for informational purposes only and does "
        "not constitute medical advice. Always consult a qualified healthcare "
        "professional for diagnosis and treatment."
    )

# ──────────────────────────────────────────────────────────────
# Main header
# ──────────────────────────────────────────────────────────────
st.title("🩺 AI-Powered Symptom Checker")
st.markdown(
    "Describe your symptoms below. The assistant will suggest a **triage level** "
    "and **possible related conditions** powered by **Gemini 2.5 Flash**."
)
st.info(
    "⚠️ This is not a substitute for professional medical advice. "
    "In a life-threatening emergency, call **911** immediately.",
    icon="ℹ️",
)

st.markdown("---")

# ──────────────────────────────────────────────────────────────
# Input form
# ──────────────────────────────────────────────────────────────
with st.form("symptom_form", clear_on_submit=False):
    st.subheader("📝 Enter Your Symptoms")

    symptoms_input = st.text_area(
        "Describe your symptoms in detail",
        height=140,
        placeholder=(
            "e.g. I have had a throbbing headache on the right side for 3 days, "
            "sensitivity to light, nausea, and occasional vomiting…"
        ),
        help="The more detail you provide, the more accurate the analysis.",
    )

    st.markdown("#### 👤 Optional Patient Context")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30, step=1)
        sex = st.selectbox(
            "Biological Sex",
            options=["Not specified", "Male", "Female", "Other"],
        )
    with col2:
        duration = st.selectbox(
            "Symptom Duration",
            options=[
                "Less than 24 hours",
                "1–3 days",
                "4–7 days",
                "1–2 weeks",
                "More than 2 weeks",
                "Not sure",
            ],
        )
        severity = st.slider(
            "Self-Rated Severity",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = very mild, 10 = worst imaginable",
        )

    submitted = st.form_submit_button("🔍 Analyse Symptoms", use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Analysis & result rendering
# ──────────────────────────────────────────────────────────────
if submitted:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar to continue.")
        st.stop()

    if not symptoms_input.strip():
        st.warning("Please describe your symptoms before submitting.")
        st.stop()

    patient_info = {
        "age": age,
        "sex": sex,
        "duration": duration,
        "severity": severity,
    }

    with st.spinner("Analysing symptoms with Gemini 2.5 Flash…"):
        try:
            result = analyse_symptoms(api_key, symptoms_input.strip(), patient_info)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
            st.stop()

    # Save to history
    st.session_state.history.append(
        {"symptoms": symptoms_input.strip(), "triage": result["triage"], "result": result}
    )

    triage_key = result["triage"]
    meta = TRIAGE_LEVELS.get(triage_key, TRIAGE_LEVELS["SEE A DOCTOR"])

    st.markdown("---")
    st.subheader("📊 Analysis Results")

    # ── Triage banner ──
    color = meta["color"]
    icon = meta["icon"]
    label = meta["label"]
    desc = meta["description"]

    if color == "green":
        st.success(f"{icon}  **Triage: {label}**\n\n{desc}")
    elif color == "orange":
        st.warning(f"{icon}  **Triage: {label}**\n\n{desc}")
    else:
        st.error(f"{icon}  **Triage: {label}**\n\n{desc}")

    # ── Possible conditions ──
    st.markdown("#### 🦠 Possible Related Conditions")
    conditions = result.get("conditions", [])
    if conditions:
        for cond in conditions:
            st.markdown(f"- {cond}")
    else:
        st.caption("No specific conditions identified.")

    # ── Clinical reasoning ──
    st.markdown("#### 🧠 Clinical Reasoning")
    st.markdown(result.get("reasoning", "—"))

    # ── Actionable advice ──
    st.markdown("#### 💊 Recommended Next Steps")
    st.markdown(result.get("advice", "—"))

    # ── Disclaimer ──
    st.markdown("---")
    st.caption(f"ℹ️ {result.get('disclaimer', '')}")

    # ── Severity indicator ──
    st.markdown("#### 📈 Reported Severity")
    st.progress(severity / 10, text=f"Severity: {severity}/10")

    # ── Emergency reminder ──
    if triage_key == "EMERGENCY":
        st.markdown("---")
        st.error(
            "🚨 **EMERGENCY REMINDER** — Do NOT wait. Call **911** or have someone "
            "drive you to the nearest emergency room NOW. Do not drive yourself."
        )

# ──────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Built with [Streamlit](https://streamlit.io) · Powered by "
    "[Google Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/) · "
    "For educational use only."
)
