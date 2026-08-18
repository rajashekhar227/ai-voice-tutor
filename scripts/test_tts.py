from app.services.tts_service import TTSService


text = """
Hello students.

Today we are going to learn about Kharif crops.

Kharif crops are crops that are sown during the rainy season.

In India, the rainy season is generally from June to September.

Some examples of Kharif crops are paddy, maize, soyabean,
groundnut and cotton.

These are important examples of crops grown during the rainy season.
"""


tts_service = TTSService()

output_path = "data/audio/kharif_crops.wav"

tts_service.generate_audio(
    text,
    output_path
)

print("\nAudio generated successfully!")
print("Saved to:", output_path)