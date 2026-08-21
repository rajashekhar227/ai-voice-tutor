import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class LLMService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    # ========================================================
    # GENERATE LESSON
    # ========================================================

    def generate_lesson(
        self,
        topic,
        content,
        language="english"
    ):

        # ----------------------------------------------------
        # Language instructions
        # ----------------------------------------------------

        language_instructions = {

            "english": """
Generate the lesson in clear, simple Indian English.
Use natural wording that Class 8 students in India
can easily understand.
Use English script.
""",

            "hindi": """
Generate the lesson in simple Hindi.
Use Devanagari script.
Use natural Hindi that Class 8 students in India
can easily understand.
Do not write Hindi using English letters.
""",

            "telugu": """
Generate the lesson in simple Telugu.
Use Telugu script.
Use natural Telugu that Class 8 students in India
can easily understand.
Do not write Telugu using English letters.
"""
        }

        # ----------------------------------------------------
        # Validate language
        # ----------------------------------------------------

        language = language.lower().strip()

        if language not in language_instructions:

            raise ValueError(
                f"Unsupported language: {language}"
            )

        language_instruction = (
            language_instructions[language]
        )

        # ----------------------------------------------------
        # Prompt
        # ----------------------------------------------------

        prompt = f"""
You are an AI voice teacher for Class 8 students.

Your job is to teach the student about the given topic
using the provided textbook content.

Topic:
{topic}

Textbook content:
{content}

Target language:
{language}

Language requirement:
{language_instruction}

Teaching instructions:

1. Explain the topic like a friendly Class 8 teacher.

2. Use simple words and short sentences.

3. Make the explanation suitable for students in India.

4. Do not copy the textbook word-for-word.

5. Explain the important ideas clearly.

6. Give examples only when they are supported by
   the provided textbook content.

7. Stay strictly within the information provided
   in the textbook content.

8. Do not add unrelated information.

9. Do not ask the student questions.

10. Do not say:
    "Does that make sense?"
    "Are you ready?"
    or similar phrases.

11. Do not expect the student to answer.

12. Avoid complicated technical language.

13. Make the lesson natural for text-to-speech.

14. Use a smooth teaching flow.

15. Do not simply list facts.

16. Explain important concepts step by step.

17. End with a short revision of the important points.

18. Do not mention that you are an AI.

19. Do not mention the textbook.

20. Do not mention these instructions.

21. Generate ONLY the lesson.

22. Do not use Markdown formatting.

23. Do not use bullet points or numbered lists,
    because the lesson will be converted into speech.

24. Keep the lesson suitable for approximately
    2 to 3 minutes of spoken audio.

Generate the complete lesson now.
"""

        # ----------------------------------------------------
        # Retry Gemini
        # ----------------------------------------------------

        max_attempts = 3

        for attempt in range(
            1,
            max_attempts + 1
        ):

            print(
                f"Generating {language} lesson "
                f"(attempt {attempt}/{max_attempts})..."
            )

            try:

                response = (
                    self.client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                )

                if not response.text:

                    raise RuntimeError(
                        "Gemini returned empty response."
                    )

                return response.text.strip()

            except Exception as error:

                print(
                    f"Generation failed: {error}"
                )

                if attempt < max_attempts:

                    print(
                        "Retrying..."
                    )

                    time.sleep(2)

                else:

                    raise