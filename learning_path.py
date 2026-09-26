import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY)


def get_learning_recommendations(topic):
    prompt = f"""
Create a simple learning path for the topic: {topic}

Give:
1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Suggested order of learning

Keep the recommendations clear and suitable for students.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text