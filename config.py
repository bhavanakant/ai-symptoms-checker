"""
Configuration and constants for the Symptom Checker application.
"""

# Gemini model identifier
GEMINI_MODEL = "gemini-2.5-flash"

# Triage levels with display metadata
TRIAGE_LEVELS = {
    "SELF-CARE": {
        "color": "green",
        "icon": "🟢",
        "label": "Self-Care at Home",
        "description": "Your symptoms appear mild. Rest, hydration, and over-the-counter remedies are likely sufficient.",
    },
    "SEE A DOCTOR": {
        "color": "orange",
        "icon": "🟡",
        "label": "Schedule a Doctor Visit",
        "description": "Your symptoms warrant professional medical evaluation. Book an appointment within 1–2 days.",
    },
    "EMERGENCY": {
        "color": "red",
        "icon": "🔴",
        "label": "Seek Emergency Care Immediately",
        "description": "Your symptoms may indicate a serious condition. Go to the nearest emergency room or call 911.",
    },
}

# System prompt fed to Gemini
SYSTEM_PROMPT = """You are a medical triage assistant. Your job is to analyse patient-reported symptoms and provide:
1. A triage recommendation (one of: SELF-CARE, SEE A DOCTOR, or EMERGENCY).
2. A list of 3–5 possible related conditions based on the symptoms.
3. A brief clinical explanation (2–3 sentences) of your reasoning.
4. Specific self-care or next-step advice matching the triage level.

IMPORTANT RULES:
- Always err on the side of caution. When in doubt, escalate the triage level.
- For any symptom involving chest pain, difficulty breathing, stroke signs (FAST), severe bleeding, loss of consciousness, or poisoning, always recommend EMERGENCY.
- Never diagnose definitively. Use language such as "may indicate", "could suggest", "possible".
- Always remind users that this tool does not replace professional medical advice.

Respond ONLY in valid JSON with this exact structure (no markdown fences, no extra text):
{
  "triage": "SELF-CARE" | "SEE A DOCTOR" | "EMERGENCY",
  "conditions": ["Condition 1", "Condition 2", "Condition 3"],
  "reasoning": "Brief clinical explanation here.",
  "advice": "Specific actionable advice for this triage level.",
  "disclaimer": "This is not a substitute for professional medical advice."
}
"""

# Few-shot examples appended to user message for grounding
FEW_SHOT_EXAMPLES = """
Examples of correct responses:

Symptoms: mild runny nose, sneezing, no fever
{"triage":"SELF-CARE","conditions":["Common cold","Allergic rhinitis","Viral rhinitis"],"reasoning":"Mild upper-respiratory symptoms without fever are consistent with a common cold or allergy flare. No red-flag signs are present.","advice":"Rest, drink plenty of fluids, use saline nasal spray, and consider OTC antihistamines or decongestants if needed.","disclaimer":"This is not a substitute for professional medical advice."}

Symptoms: persistent cough for 2 weeks, mild fever, night sweats
{"triage":"SEE A DOCTOR","conditions":["Pneumonia","Tuberculosis","Bronchitis","Sinusitis"],"reasoning":"A productive cough lasting over two weeks with low-grade fever and night sweats requires clinical evaluation to rule out lower-respiratory or systemic infection.","advice":"Book a GP appointment within 24–48 hours. Avoid contact with immunocompromised individuals until assessed.","disclaimer":"This is not a substitute for professional medical advice."}

Symptoms: sudden severe chest pain radiating to left arm, sweating, shortness of breath
{"triage":"EMERGENCY","conditions":["Acute myocardial infarction","Unstable angina","Aortic dissection","Pulmonary embolism"],"reasoning":"Classic presentation of cardiac emergency. Immediate intervention is critical to prevent permanent damage or death.","advice":"Call 911 immediately. Chew one regular aspirin (325 mg) if not allergic and not contraindicated. Do not drive yourself.","disclaimer":"This is not a substitute for professional medical advice."}
"""
