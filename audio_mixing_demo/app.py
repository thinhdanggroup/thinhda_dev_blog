from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import numpy as np
from audio_mixer import ConferenceAudioMixer
import base64
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Create our audio mixer instance
mixer = ConferenceAudioMixer()
mixer.start_mixing()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    """Handle new participant joining"""
    participant_id = data.get('participant_id')
    if participant_id:
        mixer.add_participant(participant_id)
        emit('join_response', {'status': 'success', 'message': f'Joined as {participant_id}'})

@socketio.on('leave')
def handle_leave(data):
    """Handle participant leaving"""
    participant_id = data.get('participant_id')
    if participant_id:
        mixer.remove_participant(participant_id)
        emit('leave_response', {'status': 'success', 'message': f'Left conference'})

@socketio.on('audio_data')
def handle_audio_data(data):
    """Handle incoming audio data"""
    participant_id = data.get('participant_id')
    audio_data = data.get('audio_data')
    
    if participant_id and audio_data:
        # Convert base64 audio data to numpy array
        try:
            audio_bytes = base64.b64decode(audio_data.split(',')[1])
            audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
            
            # Process the audio through our mixer
            mixer.receive_audio(participant_id, audio_array)
            
            # Get mixed audio from output buffer
            try:
                mixed_audio = mixer.output_buffer.get(timeout=0.1)
                # Convert mixed audio to base64 for sending back
                mixed_bytes = mixed_audio.astype(np.float32).tobytes()
                mixed_base64 = base64.b64encode(mixed_bytes).decode('utf-8')
                
                # Broadcast mixed audio to all participants
                emit('mixed_audio', {
                    'audio_data': f'data:audio/raw;base64,{mixed_base64}'
                }, broadcast=True)
            except Exception as e:
                print(f"Error getting mixed audio: {e}")
                
        except Exception as e:
            print(f"Error processing audio data: {e}")

@socketio.on('set_volume')
def handle_volume(data):
    """Handle volume adjustment"""
    participant_id = data.get('participant_id')
    volume = data.get('volume')
    if participant_id and volume is not None:
        mixer.set_participant_volume(participant_id, float(volume))

if __name__ == '__main__':
    socketio.run(app, debug=True)
