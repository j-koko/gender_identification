import parselmouth
import pyaudio
import wave

# Function to record audio from microphone
def record_audio(filename, duration=5, rate=44100, channels=1):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=1024)

    print("Say something in a neutral tone...")
    frames = []

    for _ in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Thank you. I finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


# Function to analyze pitch using parselmouth
def analyze_pitch(filename):
    snd = parselmouth.Sound(filename)
    pitch = snd.to_pitch()

    pitch_values = pitch.selected_array['frequency']
    pitch_values = [p for p in pitch_values if 300 > p > 60]  # Remove non-speech frequencies
    average_pitch = sum(pitch_values) / len(pitch_values) if pitch_values else 0

    return average_pitch

def is_female(persons_pitch):
    # Setting threshold
    return persons_pitch > 180

def infer_gender(filename):
    # Analyze average pitch
    average_pitch = analyze_pitch(filename)
    # Determine gender
    if is_female(average_pitch):
        return True
    else:
        return False


# Main function
if __name__ == "__main__":
    filename = "recorded_audio.wav"
    record_audio(filename, duration=5)
    is_female = infer_gender(filename)
    pitch_info = round(analyze_pitch(filename), 2)

    # Inform user about the result
    if is_female:
        print(f"You are probably a woman as your average pitch is {pitch_info} Hz.")
    else:
        print(f"You are probably a man as your average pitch is {pitch_info} Hz.")
