import os

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from dotenv import load_dotenv
load_dotenv()

deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

def convert(audio_file):
    try:
        deepgram = DeepgramClient()

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-3",
            smart_format=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        return transcript

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print(convert(r"audio\data\output.wav"))
