import numpy as np
import queue
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional
from scipy.io import wavfile
import sounddevice as sd
import os

@dataclass
class AudioStream:
    """Represents an audio stream from a participant"""
    participant_id: str
    wav_file: str
    sample_rate: int = 44100
    buffer_size: int = 1024
    is_active: bool = True
    
    def __post_init__(self):
        self.buffer = queue.Queue(maxsize=10)
        self.volume = 1.0
        self._load_wav()
        
    def _load_wav(self):
        """Load WAV file data"""
        try:
            sample_rate, data = wavfile.read(self.wav_file)
            # Convert to float32 and normalize to [-1, 1]
            if data.dtype == np.int16:
                data = data.astype(np.float32) / 32768.0
            elif data.dtype == np.int32:
                data = data.astype(np.float32) / 2147483648.0
                
            # Convert stereo to mono if needed
            if len(data.shape) > 1 and data.shape[1] > 1:
                data = np.mean(data, axis=1)
                
            self.audio_data = data
            self.sample_rate = sample_rate
            self.position = 0
            print(f"Loaded WAV file: {self.wav_file} (sr={sample_rate}Hz, length={len(data)})")
        except Exception as e:
            print(f"Error loading WAV file {self.wav_file}: {e}")
            # Create empty audio data as fallback
            self.audio_data = np.zeros(sample_rate * 5)  # 5 seconds of silence
            self.position = 0

    def get_next_chunk(self) -> Optional[np.ndarray]:
        """Get next chunk of audio data"""
        if not self.is_active or self.position >= len(self.audio_data):
            return None
            
        end_pos = min(self.position + self.buffer_size, len(self.audio_data))
        chunk = self.audio_data[self.position:end_pos]
        
        # Pad with zeros if chunk is smaller than buffer_size
        if len(chunk) < self.buffer_size:
            chunk = np.pad(chunk, (0, self.buffer_size - len(chunk)))
            
        self.position += self.buffer_size
        
        # Loop the audio when it reaches the end
        if self.position >= len(self.audio_data):
            self.position = 0
            
        return chunk * self.volume

class ConferenceAudioMixer:
    """Handles mixing of multiple audio streams in a conference"""
    
    def __init__(self, sample_rate: int = 44100, buffer_size: int = 1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.streams: Dict[str, AudioStream] = {}
        self.output_buffer = queue.Queue(maxsize=20)
        self.is_mixing = False
        self.mixing_thread = None
        self.playback_thread = None
        
        # Network quality simulation (0.0 to 1.0)
        self.network_quality = 1.0
        
    def add_participant(self, participant_id: str, wav_file: str) -> None:
        """Add a new participant to the conference"""
        if participant_id not in self.streams:
            stream = AudioStream(
                participant_id=participant_id,
                wav_file=wav_file,
                sample_rate=self.sample_rate,
                buffer_size=self.buffer_size
            )
            self.streams[participant_id] = stream
            print(f"Added participant: {participant_id}")
    
    def remove_participant(self, participant_id: str) -> None:
        """Remove a participant from the conference"""
        if participant_id in self.streams:
            self.streams[participant_id].is_active = False
            del self.streams[participant_id]
            print(f"Removed participant: {participant_id}")
    
    def start_mixing(self) -> None:
        """Start the audio mixing process"""
        if not self.is_mixing:
            self.is_mixing = True
            self.mixing_thread = threading.Thread(target=self._mix_audio)
            self.playback_thread = threading.Thread(target=self._play_audio)
            self.mixing_thread.daemon = True
            self.playback_thread.daemon = True
            self.mixing_thread.start()
            self.playback_thread.start()
            print("Started audio mixing")
    
    def stop_mixing(self) -> None:
        """Stop the audio mixing process"""
        self.is_mixing = False
        if self.mixing_thread:
            self.mixing_thread.join()
        if self.playback_thread:
            self.playback_thread.join()
        print("Stopped audio mixing")
    
    def _mix_audio(self) -> None:
        """Main mixing loop"""
        while self.is_mixing:
            try:
                # Mix audio from all active streams
                mixed_chunk = np.zeros(self.buffer_size)
                active_streams = 0
                
                for stream in self.streams.values():
                    chunk = stream.get_next_chunk()
                    if chunk is not None:
                        # Apply network quality simulation
                        if self.network_quality < 1.0:
                            noise = np.random.normal(0, 1 - self.network_quality, chunk.shape)
                            chunk = chunk + noise
                        
                        mixed_chunk += chunk
                        active_streams += 1
                
                if active_streams > 0:
                    # Normalize the mixed audio
                    mixed_chunk = mixed_chunk / active_streams
                    # Prevent clipping
                    mixed_chunk = np.clip(mixed_chunk, -1.0, 1.0)
                    
                    try:
                        self.output_buffer.put(mixed_chunk, block=False)
                    except queue.Full:
                        print("Output buffer full, dropping mixed chunk")
                
                # Small sleep to prevent CPU overload
                time.sleep(0.001)
                
            except Exception as e:
                print(f"Error in mixing loop: {e}")
    
    def _play_audio(self) -> None:
        """Playback mixed audio"""
        def audio_callback(outdata, frames, time, status):
            try:
                data = self.output_buffer.get_nowait()
                outdata[:] = data.reshape(-1, 1)
            except queue.Empty:
                outdata[:] = np.zeros((frames, 1))
        
        try:
            with sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=audio_callback,
                blocksize=self.buffer_size
            ):
                while self.is_mixing:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Error in audio playback: {e}")
    
    def set_participant_volume(self, participant_id: str, volume: float) -> None:
        """Adjust the volume for a specific participant"""
        if participant_id in self.streams:
            self.streams[participant_id].volume = max(0.0, min(1.0, volume))
    
    def set_network_quality(self, quality: float) -> None:
        """Simulate network conditions (0.0 to 1.0)"""
        self.network_quality = max(0.0, min(1.0, quality))

def create_sample_wav():
    """Create a sample WAV file with a sine wave"""
    duration = 5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a sample audio signal (combination of frequencies)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)
    
    # Ensure samples directory exists
    os.makedirs("samples", exist_ok=True)
    
    # Save multiple WAV files with different frequencies
    for i, freq_mult in enumerate([1, 1.5, 2]):
        audio = signal * np.sin(2 * np.pi * 220 * freq_mult * t)
        wavfile.write(f"samples/sample{i+1}.wav", sample_rate, (audio * 32767).astype(np.int16))
    
    return ["samples/sample1.wav", "samples/sample2.wav", "samples/sample3.wav"]

def demo_conference():
    """Demonstrate the audio mixer functionality"""
    # Create sample WAV files
    wav_files = create_sample_wav()
    
    # Create mixer instance
    mixer = ConferenceAudioMixer()
    
    # Add participants with their WAV files
    participants = ["user1", "user2", "user3"]
    for participant, wav_file in zip(participants, wav_files):
        mixer.add_participant(participant, wav_file)
    
    # Start mixing
    mixer.start_mixing()
    
    try:
        print("\nPlaying conference audio...")
        time.sleep(5)  # Play for 5 seconds
        
        # Demonstrate network quality adjustment
        print("\nSimulating poor network conditions...")
        mixer.set_network_quality(0.5)
        time.sleep(5)
        
        # Remove a participant
        print("\nRemoving user2...")
        mixer.remove_participant("user2")
        time.sleep(5)
        
        # Adjust volume of remaining participants
        print("\nAdjusting volumes...")
        mixer.set_participant_volume("user1", 0.8)
        mixer.set_participant_volume("user3", 0.6)
        time.sleep(5)
        
    finally:
        # Clean up
        mixer.stop_mixing()
        print("\nDemo completed")

if __name__ == "__main__":
    demo_conference()
