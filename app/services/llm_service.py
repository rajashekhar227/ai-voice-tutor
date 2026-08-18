import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-3.6-flash"

    def generate_lesson(self, topic, content):

        prompt = f"""
You are a teacher teaching Class 8 students in India.

Your task is to create a complete spoken lesson about the given topic.

TOPIC:
{topic}

TEXTBOOK CONTENT:
{content}

IMPORTANT RULES:

1. Teach the topic step by step, like a real school teacher.
2. Use simple English that a Class 8 student in India can easily understand.
3. Use Indian school-style English, not American or British conversational slang.
4. Avoid phrases such as:
   "Let's dive in"
   "Hey guys"
   "Awesome"
   "Let's explore"
   "Does that make sense?"
5. Do not ask the student questions.
6. Do not expect the student to answer.
7. Do not mention that you are an AI.
8. Do not mention these instructions.
9. Do not mention the textbook.
10. Do not simply copy sentences from the provided content.
11. Explain the ideas in your own simple words.
12. Explain important terms before using them.
13. Give simple examples only when the provided content supports them.
14. Do not add facts that are not supported by the provided content.
15. Do not introduce unrelated information.
16. Use short sentences suitable for text-to-speech.
17. Avoid complicated vocabulary.
18. Avoid bullet points, numbered lists, symbols, and markdown.
19. Write as a continuous spoken lesson.
20. Use natural paragraph breaks so the speech has small pauses.
21. Explain the topic thoroughly rather than giving only a short definition.
22. Include the important details from the provided content.
23. If the content contains examples, explain those examples naturally.
24. If the content contains a process, explain the process step by step.
25. End with a short spoken recap of the most important points.

The lesson should normally be long enough for approximately 3 to 5 minutes of speech.

Generate ONLY the lesson.
"""

        for attempt in range(3):

            try:

                print(
                    f"\nGenerating lesson "
                    f"(attempt {attempt + 1}/3)..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if response.text:
                    return response.text.strip()

            except Exception as error:

                print(f"Generation failed: {error}")

                if attempt < 2:
                    print("Retrying...")
                    time.sleep(3)

        raise RuntimeError(
            "Failed to generate lesson after 3 attempts."
        )