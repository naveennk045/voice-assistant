import pyaudio
import wave
import threading
import time

class AudioRecorder:
    def __init__(self):
        self.chunk = 1024 
        self.sample_format = pyaudio.paInt16  
        self.channels = 2  
        self.fs = 44100  
        self.p = pyaudio.PyAudio() 
        
    
    def record_audio(self, ):
        """
        Record audio until user presses Enter
        
        Args:
            filename (str): Name of the output WAV file
        """
        print("Recording... Press Enter to stop.")
        
        # Open stream
        stream = self.p.open(
                            format=self.sample_format,
                           channels=self.channels,
                           rate=self.fs,
                           frames_per_buffer=self.chunk,
                           input=True,
                           )
        
        frames = []
        
        # Use a thread to wait for Enter key press
        stop_recording = False
        
        def wait_for_enter():
            nonlocal stop_recording
            input()
            stop_recording = True
        
        thread = threading.Thread(target=wait_for_enter)
        thread.daemon = True
        thread.start()
        
        while not stop_recording:
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
            time.sleep(0.01)
        
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        
        print("\nRecording finished!")
        
        # Save the recorded data as a WAV file
        filename=r"audio/data/input.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"Audio saved as {filename}")
    
    def close(self):
        """Close the PyAudio interface"""
        self.p.terminate()

def main():
    recorder = AudioRecorder()
    

    recorder.record_audio()
        
    recorder.close()

if __name__ == "__main__":
    main()