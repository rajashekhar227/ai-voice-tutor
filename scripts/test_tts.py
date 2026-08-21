from app.services.tts_service import TTSService


lesson = """
Hello students. Today we are going to learn about Kharif crops.

Kharif crops are crops that are sown during the rainy season.
In India, the rainy season is generally from June to September.

Some examples of Kharif crops are paddy, maize, soyabean,
groundnut and cotton.

Remember that Kharif crops are mainly associated with the rainy
season.
"""


tts_service = TTSService()

output = tts_service.generate_audio(
    lesson,
    "data/audio/kharif_crops.wav"
)

print("\nAudio generated successfully!")
print("Saved to:", output)