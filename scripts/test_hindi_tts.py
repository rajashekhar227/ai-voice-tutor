from pathlib import Path

from app.services.tts_service import TTSService


text = """
आज हम खरीफ फसलों के बारे में समझेंगे।

जो फसलें बारिश के मौसम में बोई जाती हैं,
उन्हें खरीफ फसलें कहते हैं।

भारत में बारिश का मौसम आमतौर पर जून से सितंबर तक होता है।

धान, मक्का, सोयाबीन, मूंगफली और कपास
खरीफ फसलों के मुख्य उदाहरण हैं।

धान को बहुत अधिक पानी की आवश्यकता होती है।
इसीलिए इसे बारिश के मौसम में उगाया जाता है।
"""


model = "hi_IN-priyamvada-medium.onnx"

output = Path(
    "data/audio/test_hindi.wav"
)


tts = TTSService(model)

tts.generate_audio(
    text,
    output
)

print("\nHindi test complete.")
print("Audio:", output)