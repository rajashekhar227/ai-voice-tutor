import re
import subprocess
import sys
import wave
from pathlib import Path


class TTSService:

    def __init__(self, model_path):

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

    # ---------------------------------------------------------
    # CLEAN TEXT
    # ---------------------------------------------------------

    def clean_text(self, text):

        # Remove invalid surrogate characters
        text = text.encode(
            "utf-8",
            errors="ignore"
        ).decode(
            "utf-8",
            errors="ignore"
        )

        # Remove control characters except newline
        text = "".join(
            char
            for char in text
            if char == "\n"
            or char == "\r"
            or char == "\t"
            or ord(char) >= 32
        )

        # Remove markdown
        text = re.sub(r"\*\*", "", text)
        text = re.sub(r"\*", "", text)
        text = re.sub(r"`", "", text)

        # Convert multiple spaces to one
        text = re.sub(r"[ \t]+", " ", text)

        # Convert multiple newlines
        text = re.sub(r"\n+", "\n", text)

        return text.strip()

    # ---------------------------------------------------------
    # SPLIT TEXT
    # ---------------------------------------------------------

    def split_text(self, text, max_chars=350):

        text = self.clean_text(text)

        # Split using sentence endings
        sentences = re.split(
            r"(?<=[.!?।॥])\s+",
            text
        )

        chunks = []

        current = ""

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # If adding sentence is still small enough
            if len(current) + len(sentence) + 1 <= max_chars:

                if current:
                    current += " "

                current += sentence

            else:

                if current:
                    chunks.append(current)

                current = sentence

        if current:
            chunks.append(current)

        return chunks

    # ---------------------------------------------------------
    # GENERATE SINGLE WAV
    # ---------------------------------------------------------

    def generate_single_audio(
        self,
        text,
        output_path
    ):

        text_file = output_path.with_suffix(".txt")

        # UTF-8 text file
        with open(
            text_file,
            "w",
            encoding="utf-8",
            newline="\n"
        ) as file:

            file.write(text)

        command = [
            sys.executable,
            "-m",
            "piper",

            "-m",
            str(self.model_path),

            "-i",
            str(text_file),

            "-f",
            str(output_path)
        ]

        print("\nRunning Piper:")
        print(" ".join(command))

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # Delete temporary text file
        if text_file.exists():
            text_file.unlink()

        if result.returncode != 0:

            print("\nPiper error:")
            print(result.stderr)

            if output_path.exists():
                output_path.unlink()

            raise RuntimeError(
                "Piper failed to generate audio."
            )

        if not output_path.exists():
            raise RuntimeError(
                "Piper did not create the WAV file."
            )

        if output_path.stat().st_size < 1000:

            output_path.unlink()

            raise RuntimeError(
                "Piper created an invalid WAV file."
            )

    # ---------------------------------------------------------
    # COMBINE WAV FILES
    # ---------------------------------------------------------

    def combine_wav_files(
        self,
        wav_files,
        output_path
    ):

        if not wav_files:
            raise RuntimeError(
                "No WAV files to combine."
            )

        with wave.open(
            str(wav_files[0]),
            "rb"
        ) as first:

            params = first.getparams()

            frames = [
                first.readframes(
                    first.getnframes()
                )
            ]

        # Read remaining files
        for wav_file in wav_files[1:]:

            with wave.open(
                str(wav_file),
                "rb"
            ) as audio:

                # Make sure format matches
                if (
                    audio.getnchannels()
                    != params.nchannels
                    or
                    audio.getsampwidth()
                    != params.sampwidth
                    or
                    audio.getframerate()
                    != params.framerate
                ):

                    raise RuntimeError(
                        "WAV files have different audio formats."
                    )

                frames.append(
                    audio.readframes(
                        audio.getnframes()
                    )
                )

        # Write final WAV
        with wave.open(
            str(output_path),
            "wb"
        ) as output:

            output.setparams(params)

            for frame in frames:
                output.writeframes(frame)

    # ---------------------------------------------------------
    # MAIN FUNCTION
    # ---------------------------------------------------------

    def generate_audio(
        self,
        text,
        output_path
    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        print("\nCleaning text...")

        text = self.clean_text(text)

        # -----------------------------------------------------
        # Split long lesson
        # -----------------------------------------------------

        chunks = self.split_text(
            text,
            max_chars=350
        )

        print(
            f"Text split into {len(chunks)} audio segments."
        )

        temporary_files = []

        try:

            # -------------------------------------------------
            # Generate each segment
            # -------------------------------------------------

            for i, chunk in enumerate(chunks):

                print(
                    f"\nGenerating audio segment "
                    f"{i + 1}/{len(chunks)}..."
                )

                temp_file = (
                    output_path.parent
                    /
                    f"{output_path.stem}_part_{i}.wav"
                )

                self.generate_single_audio(
                    chunk,
                    temp_file
                )

                temporary_files.append(
                    temp_file
                )

            # -------------------------------------------------
            # Combine
            # -------------------------------------------------

            print("\nCombining audio segments...")

            self.combine_wav_files(
                temporary_files,
                output_path
            )

            print(
                "\nFinal audio created:"
            )

            print(output_path)

        finally:

            # -------------------------------------------------
            # Remove temporary WAV files
            # -------------------------------------------------

            for file in temporary_files:

                if file.exists():
                    file.unlink()