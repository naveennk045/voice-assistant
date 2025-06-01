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

SPEAK_TEXT = {"text": "Hello world!"}
filename = "test.wav"

def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient()

        # STEP 2 Call the save method on the speak property
        options = SpeakOptions(
            model="aura-2-thalia-en",
        )

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
