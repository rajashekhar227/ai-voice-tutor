import json
from pathlib import Path

from app.services.lesson_service import LessonService


knowledge_path = Path("data/knowledge/class_8/science")

with open(knowledge_path / "chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)


lesson_service = LessonService()

lesson = lesson_service.create_lesson(chunks[:3])

print("\nLESSON")
print("=" * 60)
print(lesson)