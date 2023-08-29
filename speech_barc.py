import pyaudio
import speech_recognition as sr

def record_audio():
    # Create a PyAudio object
    pa = pyaudio.PyAudio()

    # Open the microphone
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    frames_per_buffer = 1024
    stream = pa.open(format=audio_format, channels=channels, rate=rate, frames_per_buffer=frames_per_buffer, input=True)

    # Record audio
    audio_data = stream.read(frames_per_buffer)

    # Close the stream
    stream.close()

    # Stop the PyAudio object
    pa.terminate()

    return audio_data

def convert_audio_to_text():
    # Create a speech recognition object
    recognizer = sr.Recognizer()

    # Record audio
    audio_data = record_audio()

    # Convert audio to text
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Unable to recognize speech"
    except sr.RequestError as e:
        text = "Error: {0}".format(e)

    return text

# Create a button
button = Button(text="Record", command=record_audio)

# Bind the button click event to the functions to record and convert the audio
button.on_click(record_audio)
button.on_click(convert_audio_to_text)

# Show the button
button.pack()
