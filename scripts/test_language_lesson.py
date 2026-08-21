from pathlib import Path

from app.services.topic_lesson_service import TopicLessonService


SUBJECT = "hesc1dd"
TOPIC = "Kharif Crops"

KNOWLEDGE_PATH = Path(
    "data/knowledge/class_8"
) / SUBJECT

AUDIO_PATH = Path(
    "data/audio"
)

INDEX_PATH = (
    KNOWLEDGE_PATH
    /
    f"{SUBJECT}.index"
)

CHUNKS_PATH = (
    KNOWLEDGE_PATH
    /
    "chunks.json"
)


service = TopicLessonService(
    subject=SUBJECT,
    knowledge_path=KNOWLEDGE_PATH,
    index_path=INDEX_PATH,
    chunks_path=CHUNKS_PATH,
    audio_path=AUDIO_PATH
)


# ============================================================
# TEST ENGLISH
# ============================================================

result = service.create_lesson(
    topic=TOPIC,
    language="telugu",
)

print("\n\nLESSON")
print("=" * 60)

print(result["lesson"])

print("\nAUDIO:")
print(result["audio"])