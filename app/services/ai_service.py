import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_case(age, gender, symptoms, duration=None):
    try:
        prompt = f"""
You are a clinical AI assistant.

Patient:
Age: {age}
Gender: {gender}
Symptoms: {", ".join(symptoms)}
Duration: {duration}

Return ONLY valid JSON in this format:

[
  {{"name": "Condition name", "probability": 0.65}},
  {{"name": "Condition name", "probability": 0.25}},
  {{"name": "Condition name", "probability": 0.10}}
]

Probabilities must sum to 1.
Return only JSON.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        content = response.choices[0].message.content

        try:
            result = json.loads(content)

            # ✅ Probability validation INSIDE function
            total_prob = sum(item["probability"] for item in result)

            if not 0.99 <= total_prob <= 1.01:
                raise ValueError("Probabilities do not sum to 1")

            return result

        except json.JSONDecodeError:
            raise ValueError("Model returned invalid JSON")

    except Exception as e:
        raise e