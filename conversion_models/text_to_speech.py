import os
import logging
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)
from dotenv import load_dotenv
load_dotenv()

deepgram = DeepgramClient(os.getenv("DEEPGRAM_API_KEY"))

filename = "audio/data/output.wav"

def covert(data):
    try:
        deepgram = DeepgramClient()

        options = SpeakOptions(
            model="aura-2-thalia-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, data, options)
        print(response.to_json(indent=4))
        
        return "Audio saved to:" + filename

    except Exception as e:
        return f"Exception: {e}"

if __name__ == "__main__":
    covert({"text": "Hello world!"})