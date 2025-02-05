# Audio Mixing Demo for Large Conferences

This demo implements a server-side audio mixing solution for large conferences. It showcases key concepts of audio mixing in a conference setting, including real-time stream processing, buffer management, and network quality simulation.

## Features

- Real-time mixing of WAV audio files
- Dynamic participant management (add/remove)
- Per-participant volume control
- Network quality simulation
- Buffer management for latency handling
- Automatic audio normalization and clipping prevention
- WAV file loading and playback
- Support for different audio formats (16-bit, 32-bit)
- Automatic stereo to mono conversion

## Requirements

- Python 3.7+
- NumPy
- SciPy (for WAV file handling)
- sounddevice (for audio playback)

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

There are two ways to run the demo:

### 1. Command Line Demo
Run the basic audio mixing simulation:
```bash
python audio_mixer.py
```

This will:
1. Create sample WAV files with different frequencies
2. Load and mix these WAV files in real-time
3. Play the mixed audio through your system's speakers
4. Demonstrate network quality simulation
5. Show participant management (adding/removing)
6. Demonstrate volume control

### 2. Interactive Web Interface
Run the web interface for real audio mixing:
```bash
python app.py
```

Then open your browser to `http://localhost:5000`. The web interface allows you to:
- Join/leave the conference with your name
- Start/stop your audio stream
- Adjust your volume
- Experience real-time audio mixing with other participants

To test with multiple participants:
1. Open multiple browser windows to `http://localhost:5000`
2. Join with different names in each window
3. Start audio in each window to participate in the conference

## Code Structure

- `AudioStream`: Class representing an individual participant's audio stream
  - Manages buffer for incoming audio chunks
  - Controls individual stream volume

- `ConferenceAudioMixer`: Main mixing engine
  - Handles multiple participant streams
  - Performs real-time audio mixing
  - Manages network quality simulation
  - Controls output buffering

## Key Implementation Details

1. **Buffer Management**
   - Uses queue.Queue for thread-safe buffer operations
   - Implements maximum buffer sizes to prevent memory issues
   - Handles buffer overflow gracefully

2. **Audio Mixing**
   - Combines multiple audio streams with proper normalization
   - Prevents audio clipping
   - Applies per-participant volume control

3. **Network Simulation**
   - Simulates network quality degradation
   - Adds controlled noise to audio streams
   - Demonstrates handling of poor network conditions

4. **Thread Safety**
   - Uses threading for continuous mixing
   - Implements proper thread cleanup
   - Handles concurrent access to shared resources

## Example Output

When running the demo, you'll see:
```
Added participant: user1
Added participant: user2
Added participant: user3
Started audio mixing

Simulating conference...
Mixed audio max amplitude: 0.707
Mixed audio max amplitude: 0.707
Mixed audio max amplitude: 0.707
...

Simulating poor network conditions...
[Network quality reduced to 50%]

Removing user2...
[Participant removed, mixing continues with remaining users]

Demo completed
```

## Limitations

- Uses simulated audio data (sine waves) instead of real audio input
- Network simulation is simplified for demonstration purposes
- No actual network transmission implementation

## Future Improvements

- Add real audio input/output support
- Implement actual network transmission
- Add more sophisticated network quality simulation
- Include audio compression/decompression
- Add support for different audio formats
