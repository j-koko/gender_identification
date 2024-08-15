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

    print("Recording...")
    frames = []

    for _ in range(0, int(rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Finished recording.")

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
    pitch_values = [p for p in pitch_values if p > 0]  # Remove unvoiced parts (zero frequency)

    highest_pitch = max(pitch_values)
    lowest_pitch = min(pitch_values)
    average_pitch = sum(pitch_values) / len(pitch_values) if pitch_values else 0

    return highest_pitch, lowest_pitch, average_pitch


# Main function
if __name__ == "__main__":
    filename = "recorded_audio.wav"

    # Record audio
    record_audio(filename, duration=5)

    # Analyze pitch
    highest_pitch, lowest_pitch, average_pitch = analyze_pitch(filename)

    print(f"Highest Pitch: {highest_pitch} Hz")
    print(f"Lowest Pitch: {lowest_pitch} Hz")
    print(f"Average Pitch: {average_pitch} Hz")
