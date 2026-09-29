"""
Symptom analysis module — interfaces with Gemini 2.5 Flash to perform
AI-powered triage and condition identification.
"""

import json
import re
import google.generativeai as genai

from config import GEMINI_MODEL, SYSTEM_PROMPT, FEW_SHOT_EXAMPLES


def _extract_json(raw: str) -> dict:
    """
    Extract and parse the first JSON object found in a raw string.
    Handles cases where the model wraps its response in markdown fences.
    """
    # Strip markdown code fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()

    # Find the first { ... } block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response.")

    return json.loads(match.group())


def analyse_symptoms(api_key: str, symptoms: str, patient_info: dict) -> dict:
    """
    Send symptoms and patient context to Gemini 2.5 Flash and return
    a structured triage result.

    Parameters
    ----------
    api_key     : Gemini API key from user input.
    symptoms    : Free-text symptom description from the user.
    patient_info: Dict with keys 'age', 'sex', 'duration', 'severity'.

    Returns
    -------
    dict with keys: triage, conditions, reasoning, advice, disclaimer
    """
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
    )

    # Build the user message with patient context
    age = patient_info.get("age", "Not specified")
    sex = patient_info.get("sex", "Not specified")
    duration = patient_info.get("duration", "Not specified")
    severity = patient_info.get("severity", "Not specified")

    user_message = f"""Patient information:
- Age: {age}
- Biological sex: {sex}
- Symptom duration: {duration}
- Self-rated severity (1–10): {severity}

Reported symptoms:
{symptoms}

{FEW_SHOT_EXAMPLES}

Now analyse the patient's symptoms above and respond with ONLY valid JSON.
"""

    response = model.generate_content(user_message)
    raw_text = response.text

    result = _extract_json(raw_text)

    # Validate required keys
    required_keys = {"triage", "conditions", "reasoning", "advice", "disclaimer"}
    missing = required_keys - set(result.keys())
    if missing:
        raise ValueError(f"Model response missing keys: {missing}")

    # Normalise triage to uppercase
    result["triage"] = result["triage"].upper().strip()
    if result["triage"] not in ("SELF-CARE", "SEE A DOCTOR", "EMERGENCY"):
        raise ValueError(f"Unexpected triage value: {result['triage']}")

    return result
