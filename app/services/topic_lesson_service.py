from pathlib import Path
import re

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService


class TopicLessonService:

    def __init__(
        self,
        subject,
        knowledge_path,
        index_path,
        chunks_path,
        audio_path
    ):

        self.subject = subject

        self.knowledge_path = Path(knowledge_path)
        self.index_path = Path(index_path)
        self.chunks_path = Path(chunks_path)
        self.audio_path = Path(audio_path)

        self.audio_path.mkdir(
            parents=True,
            exist_ok=True
        )

        print("\nCreating services...")

        self.embedding_service = EmbeddingService()

        self.vector_service = VectorService(
            dimension=384
        )

        self.vector_service.load_index(
            self.index_path
        )

        self.llm_service = LLMService()

    # ========================================================
    # LANGUAGE SETTINGS
    # ========================================================

    LANGUAGE_SETTINGS = {

        "english": {
            "model": "en_US-lessac-medium.onnx",
            "suffix": "english"
        },

        "hindi": {
            "model": "hi_IN-priyamvada-medium.onnx",
            "suffix": "hindi"
        },

        "telugu": {
            "model": "te_IN-venkatesh-medium.onnx",
            "suffix": "telugu"
        }
    }

    # ========================================================
    # LOAD CHUNKS
    # ========================================================

    def load_chunks(self):

        import json

        with open(
            self.chunks_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # ========================================================
    # SEARCH TEXTBOOK
    # ========================================================

    def retrieve_content(
        self,
        topic,
        top_k=10,
        max_chunks=6
    ):

        chunks = self.load_chunks()

        print(
            f"\nSearching textbook for: {topic}"
        )

        query_embedding = (
            self.embedding_service.model.encode(
                topic
            )
        )

        distances, indices = (
            self.vector_service.search(
                query_embedding,
                top_k=top_k
            )
        )

        selected_chunks = []

        exercise_phrases = [
            "give two examples",
            "write a paragraph",
            "explain how",
            "what is irrigation",
            "complete the following",
            "word puzzle",
            "extended learning",
            "activities and projects",
            "project work",
            "fill in the blanks"
        ]

        harvesting_words = [
            "harvesting",
            "threshing",
            "winnowing",
            "combine"
        ]

        for index in indices:

            if index == -1:
                continue

            if index >= len(chunks):
                continue

            chunk = chunks[index]

            lower_chunk = chunk.lower()

            # --------------------------------------------
            # Remove exercise-heavy chunks
            # --------------------------------------------

            exercise_count = sum(
                phrase in lower_chunk
                for phrase in exercise_phrases
            )

            if exercise_count >= 2:
                continue

            # --------------------------------------------
            # Remove unrelated harvesting chunks
            # --------------------------------------------

            harvesting_count = sum(
                word in lower_chunk
                for word in harvesting_words
            )

            if (
                harvesting_count >= 3
                and "kharif crops" not in lower_chunk
            ):
                continue

            selected_chunks.append(chunk)

            if len(selected_chunks) >= max_chunks:
                break

        return selected_chunks

    # ========================================================
    # GENERATE LESSON
    # ========================================================

    def generate_lesson(
        self,
        topic,
        language,
        content
    ):

        language = language.lower()

        if language not in self.LANGUAGE_SETTINGS:

            raise ValueError(
                f"Unsupported language: {language}"
            )

        print(
            f"\nGenerating {language} lesson..."
        )

        lesson = self.llm_service.generate_lesson(
            topic=topic,
            content=content,
            language=language
        )

        return lesson

    # ========================================================
    # GENERATE AUDIO
    # ========================================================

    def generate_audio(
        self,
        topic,
        lesson,
        language
    ):

        language = language.lower()

        if language not in self.LANGUAGE_SETTINGS:

            raise ValueError(
                f"Unsupported language: {language}"
            )

        settings = self.LANGUAGE_SETTINGS[
            language
        ]

        model = settings["model"]
        suffix = settings["suffix"]

        safe_topic = re.sub(
            r"[^a-zA-Z0-9]+",
            "_",
            topic
        ).strip("_").lower()

        output_path = (
            self.audio_path
            /
            f"{self.subject}_{safe_topic}_{suffix}.wav"
        )

        print(
            f"\nGenerating {language} audio..."
        )

        tts_service = TTSService(
            model
        )

        tts_service.generate_audio(
            lesson,
            output_path
        )

        return output_path

    # ========================================================
    # COMPLETE LESSON
    # ========================================================

    def create_lesson(
        self,
        topic,
        language
    ):

        print("\n" + "=" * 60)

        print(
            f"CREATING {language.upper()} LESSON"
        )

        print("=" * 60)

        # ----------------------------------------------------
        # Retrieve textbook content
        # ----------------------------------------------------

        selected_chunks = self.retrieve_content(
            topic
        )

        print(
            "\nSelected chunks:",
            len(selected_chunks)
        )

        # ----------------------------------------------------
        # Combine chunks
        # ----------------------------------------------------

        content = "\n\n".join(
            selected_chunks
        )

        # ----------------------------------------------------
        # Generate lesson
        # ----------------------------------------------------

        lesson = self.generate_lesson(
            topic,
            language,
            content
        )

        # ----------------------------------------------------
        # Generate audio
        # ----------------------------------------------------

        audio_path = self.generate_audio(
            topic,
            lesson,
            language
        )

        return {
            "subject": self.subject,
            "topic": topic,
            "language": language,
            "lesson": lesson,
            "audio": str(audio_path),
            "selected_chunks": len(
                selected_chunks
            )
        }