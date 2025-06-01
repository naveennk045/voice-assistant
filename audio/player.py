import pyaudio
import wave
import os
import time

class AudioPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.chunk = 1024
        
    def play_audio(self, filename):
        """
        Play audio from WAV file
        
        Args:
            filename (str): Path to the WAV file
        """
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return False
            
        try:
            # Open wave file
            wf = wave.open(filename, 'rb')
            
            # Get audio properties
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()
            framerate = wf.getframerate()
            frames = wf.getnframes()
            
            # Calculate duration
            duration = frames / float(framerate)
            
            print(f"Playing: {filename}")
            print(f"Duration: {duration:.2f} seconds")
            print(f"Channels: {channels}")
            print(f"Sample Rate: {framerate} Hz")
            print(f"Sample Width: {sample_width} bytes")
            print("-" * 40)
            
            # Open stream for playback
            stream = self.p.open(format=self.p.get_format_from_width(sample_width),
                               channels=channels,
                               rate=framerate,
                               output=True)
            
            # Read and play audio data
            data = wf.readframes(self.chunk)
            start_time = time.time()
            
            while data:
                stream.write(data)
                data = wf.readframes(self.chunk)
                
                # Show progress
                elapsed = time.time() - start_time
                progress = (elapsed / duration) * 100
                print(f"\rProgress: {progress:.1f}% [{elapsed:.1f}s / {duration:.1f}s]", end='', flush=True)
            
            print(f"\rPlayback completed! [{duration:.1f}s / {duration:.1f}s]")
            
            # Close everything
            stream.stop_stream()
            stream.close()
            wf.close()
            
            return True
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    def close(self):
        """Close the PyAudio interface"""
        self.p.terminate()
    

def main():
    player = AudioPlayer()
    
    player.play_audio("audio\data\output.wav")
    player.close()

if __name__ == "__main__":
    main()