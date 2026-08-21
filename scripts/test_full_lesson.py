import json
import re
from pathlib import Path

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService
from app.services.tts_service import TTSService


# ============================================================
# SETTINGS
# ============================================================

SUBJECT = "hesc1dd"
TOPIC = "Kharif Crops"

KNOWLEDGE_PATH = Path("data/knowledge/class_8") / SUBJECT
AUDIO_PATH = Path("data/audio")

INDEX_PATH = KNOWLEDGE_PATH / f"{SUBJECT}.index"
CHUNKS_PATH = KNOWLEDGE_PATH / "chunks.json"

TOP_K = 8
MAX_CHUNKS = 3


# ============================================================
# VOICE MODELS
# ============================================================

VOICE_MODELS = {

    "English":
        "en_US-lessac-medium.onnx",

    "Hindi":
        "hi_IN-priyamvada-medium.onnx",

    "Telugu":
        "te_IN-venkatesh-medium.onnx"
}


# ============================================================
# CREATE AUDIO DIRECTORY
# ============================================================

AUDIO_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

print("\nLoading knowledge base...")

with open(
    CHUNKS_PATH,
    "r",
    encoding="utf-8"
) as file:

    chunks = json.load(file)

print("Total chunks:", len(chunks))


# ============================================================
# CREATE EMBEDDING
# ============================================================

print("\nCreating query embedding...")

embedding_service = EmbeddingService()

query_embedding = embedding_service.model.encode(
    TOPIC
)


# ============================================================
# LOAD FAISS INDEX
# ============================================================

print("\nLoading FAISS index...")

vector_service = VectorService(
    dimension=384
)

vector_service.load_index(
    INDEX_PATH
)


# ============================================================
# SEARCH
# ============================================================

print(
    "\nSearching for topic:",
    TOPIC
)

distances, indices = vector_service.search(
    query_embedding,
    top_k=TOP_K
)


# ============================================================
# FILTER CHUNKS
# ============================================================

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
    "fill in the blanks",
    "choose the correct",
    "match the following",
    "answer the following"
]


topic_keywords = [

    "kharif crops",
    "kharif crop",
    "rainy season",
    "june to september",
    "paddy",
    "maize",
    "soyabean",
    "groundnut",
    "cotton",
    "rabi crops"
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


    # --------------------------------------------------------
    # Remove exercise-heavy chunks
    # --------------------------------------------------------

    exercise_count = 0

    for phrase in exercise_phrases:

        if phrase in lower_chunk:
            exercise_count += 1

    if exercise_count >= 2:
        continue


    # --------------------------------------------------------
    # Topic relevance
    # --------------------------------------------------------

    topic_score = sum(
        keyword in lower_chunk
        for keyword in topic_keywords
    )

    if topic_score == 0:
        continue


    # --------------------------------------------------------
    # Remove harvesting-heavy chunks
    # --------------------------------------------------------

    harvesting_count = sum(
        word in lower_chunk
        for word in harvesting_words
    )

    if (
        harvesting_count >= 3
        and "kharif crops" not in lower_chunk
    ):
        continue


    # --------------------------------------------------------
    # Keep chunk
    # --------------------------------------------------------

    selected_chunks.append(chunk)

    if len(selected_chunks) >= MAX_CHUNKS:
        break


# ============================================================
# DISPLAY SELECTED CHUNKS
# ============================================================

print("\nSELECTED CHUNKS")
print("=" * 60)

print(
    "Number of chunks:",
    len(selected_chunks)
)

for i, chunk in enumerate(
    selected_chunks
):

    print(
        f"\nChunk {i + 1}"
    )

    print("-" * 60)

    print(
        chunk[:700]
    )


# ============================================================
# COMBINE SOURCE MATERIAL
# ============================================================

content = "\n\n".join(
    selected_chunks
)


# ============================================================
# CREATE SERVICES
# ============================================================

print("\nCreating services...")

llm_service = LLMService()


# ============================================================
# SAFE TOPIC NAME
# ============================================================

safe_topic = re.sub(
    r"[^a-zA-Z0-9]+",
    "_",
    TOPIC
).strip("_").lower()


# ============================================================
# GENERATE LESSONS
# ============================================================

languages = [
    "English",
    "Hindi",
    "Telugu"
]


generated_lessons = {}


for language in languages:

    print("\n")
    print("=" * 60)

    print(
        f"GENERATING {language.upper()} LESSON"
    )

    print("=" * 60)


    lesson = llm_service.generate_lesson(
        topic=TOPIC,
        content=content,
        language=language
    )


    generated_lessons[
        language
    ] = lesson


    print("\nLESSON")
    print("-" * 60)

    print(lesson)


# ============================================================
# GENERATE AUDIO
# ============================================================

print("\n")
print("=" * 60)

print("GENERATING AUDIO")

print("=" * 60)


for language in languages:

    print(
        f"\nGenerating {language} audio..."
    )


    model_path = VOICE_MODELS[
        language
    ]


    model_file = Path(
        model_path
    )


    if not model_file.exists():

        raise FileNotFoundError(
            f"Voice model not found: "
            f"{model_path}"
        )


    tts_service = TTSService(
        model_path
    )


    language_name = (
        language.lower()
    )


    output_path = (
        AUDIO_PATH /
        f"{SUBJECT}_{safe_topic}_{language_name}.wav"
    )


    tts_service.generate_audio(
        generated_lessons[language],
        output_path
    )


    print(
        f"{language} audio created:"
    )

    print(
        output_path
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 60)

print(
    "MULTILINGUAL LESSON GENERATION COMPLETE"
)

print("=" * 60)

print(
    "Subject:",
    SUBJECT
)

print(
    "Topic:",
    TOPIC
)

print(
    "Selected chunks:",
    len(selected_chunks)
)

print("\nAudio files:")

for language in languages:

    language_name = (
        language.lower()
    )

    output_path = (
        AUDIO_PATH /
        f"{SUBJECT}_{safe_topic}_{language_name}.wav"
    )

    print(
        f"{language}: {output_path}"
    )