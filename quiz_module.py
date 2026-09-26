import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_quiz(topic):
    prompt = f"""
Create a short quiz for a student about the following topic:

Topic: {topic}

Create 5 multiple-choice questions.

For each question provide:
- The question
- 4 options labeled A, B, C, D
- The correct answer
- A short explanation

Keep the questions clear and suitable for students.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text