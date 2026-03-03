import os
import json
from openai import OpenAI

# Load API key safely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_skills_from_jd(jd_text: str):
    """
    Extract skills and experience from JD using OpenAI.
    Always returns a dictionary, never crashes.
    """

    prompt = f"""
    Extract key skills and experience level from the job description below.

    Respond ONLY in valid JSON format:
    {{
      "skills": ["Java", "REST APIs"],
      "experience": "2-4 years"
    }}

    Job Description:
    {jd_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Try parsing JSON
        return json.loads(content)

    except json.JSONDecodeError:
        # OpenAI responded with text instead of JSON
        return {
            "skills": [],
            "experience": ""
        }

    except Exception as e:
        # Any OpenAI / network / auth error
        return {
            "skills": [],
            "experience": "",
            "error": str(e)
        }