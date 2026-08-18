from app.services.llm_service import LLMService


llm_service = LLMService()

context = """
The crops which are sown in the rainy season are called kharif crops.
The rainy season in India is generally from June to September.
Paddy, maize, soyabean, groundnut and cotton are kharif crops.
"""

lesson = llm_service.generate_lesson(
    "Kharif Crops",
    context
)

print("\nGENERATED LESSON")
print("=" * 60)
print(lesson)