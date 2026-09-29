# 🩺 AI-Powered Symptom Checker

An intelligent medical triage assistant built with **Streamlit** and **Google Gemini 2.5 Flash**. Users describe their symptoms and receive:

- ✅ A **triage recommendation** — Self-Care, See a Doctor, or Emergency
- 🦠 **3–5 possible related conditions**
- 🧠 **Clinical reasoning** behind the recommendation
- 💊 **Actionable next-step advice**

> ⚠️ **Disclaimer:** This tool is for informational/educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

---

## 🗂️ Project Structure

```
symptom-checker/
├── app.py            # Streamlit UI — main entry point
├── analyser.py       # Gemini 2.5 Flash integration & JSON parsing
├── config.py         # Constants, prompts, triage metadata
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable template
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone / navigate to the project
```bash
cd symptom-checker
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in and create a free API key
3. Copy the key

### 5. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.  
Paste your Gemini API key in the **sidebar** when prompted.

---

## 🧩 How It Works

```
User Input (symptoms + patient context)
        │
        ▼
  analyser.py  ──►  Gemini 2.5 Flash  ──►  Structured JSON response
        │
        ▼
  Triage level + Conditions + Reasoning + Advice
        │
        ▼
  Streamlit UI renders colour-coded result card
```

1. The user fills in the symptom text area and optional patient details (age, sex, duration, severity).
2. `analyser.py` constructs a detailed prompt with a system instruction and few-shot examples.
3. Gemini 2.5 Flash returns a strict JSON response.
4. `app.py` renders the result with colour-coded banners (green / amber / red) matching the triage level.
5. Each session is saved to **sidebar history** for quick reference.

---

## 🛡️ Triage Levels

| Level | Colour | Meaning |
|-------|--------|---------|
| 🟢 Self-Care | Green | Mild symptoms; rest and OTC remedies are sufficient |
| 🟡 See a Doctor | Amber | Warrants professional evaluation within 1–2 days |
| 🔴 Emergency | Red | Potentially life-threatening; call 911 immediately |

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push the `symptom-checker/` folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect the repo.
3. Set **Main file path** to `app.py`.
4. Under **Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```
   *(Users can also enter the key in-app via the sidebar.)*
5. Click **Deploy**.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `google-generativeai` | Gemini 2.5 Flash API client |
| `python-dotenv` | Optional `.env` file loading |

---

## 📄 License

MIT — for educational use only. Not for clinical deployment.
