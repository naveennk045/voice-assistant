from audio import player 
from audio import recorder
from llm import llm
from conversion_models import text_to_speech    
from conversion_models import speech_to_text

# recorder -> STT -> LLM -> TTS -> player

# Main script to record and play audio
recorder = recorder.AudioRecorder()
recorder.record_audio()
recorder.close()

text=speech_to_text.convert(r"audio\data\input.wav")
print(f"Recognized text: {text}")

llm_response = llm.chat(text)
print(f"LLM response: {llm_response}")


text_to_speech.covert({"text": llm_response})

player = player.AudioPlayer()

player.play_audio(r"audio/data/output.wav")
player.close()
