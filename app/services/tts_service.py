from pathlib import Path
import subprocess
import sys


class TTSService:

    def __init__(self):

        self.model_path = Path(
            "en_US-lessac-medium.onnx"
        )

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Piper model not found: {self.model_path}"
            )

    def generate_audio(self, text, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [
            sys.executable,
            "-m",
            "piper",
            "-m",
            str(self.model_path),
            "-f",
            str(output_path)
        ]

        subprocess.run(
            command,
            input=text,
            text=True,
            check=True
        )

        return output_path