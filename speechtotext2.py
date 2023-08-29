import tkinter as tk
import threading
import speech_recognition as sr
from textblob import TextBlob

class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text and Sentiment Analysis")
        
        self.record_button = tk.Button(root, text="Record", command=self.start_recording)
        self.record_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state="disabled")
        self.stop_button.pack(pady=10)
        
        self.text_display = tk.Text(root, height=10, width=40)
        self.text_display.pack(padx=10, pady=10)
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recording_thread = None
        self.audio = None
        self.should_record = True  # Flag to control recording
        self.texts = []  # List to store recognized text
        
    def start_recording(self):
        self.record_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, "Recording...")
        
        self.audio = []
        self.should_record = True  # Set flag to start recording
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()
        
    def record_audio(self):
        with self.microphone as source:
            while self.should_record:  # Check the flag to continue recording
                audio_chunk = self.recognizer.listen(source)
                self.audio.append(audio_chunk)
        
    def stop_recording(self):
        self.should_record = False  # Set flag to stop recording
        
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join()  # Wait for the recording thread to finish
            
        self.stop_button.config(state="disabled")
        self.record_button.config(state="normal")
        self.process_audio()
        self.audio = []
        
    def process_audio(self):
        full_audio = sr.AudioData(b''.join([chunk.frame_data for chunk in self.audio]), self.microphone.SAMPLE_RATE, self.microphone.SAMPLE_WIDTH)
        
        try:
            text = self.recognizer.recognize_google(full_audio)
            self.texts.append(text)  # Store recognized text
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, text)
            self.perform_sentiment_analysis(text)
        except sr.UnknownValueError:
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "Could not understand audio")
        except sr.RequestError as e:
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"Could not request results; {e}")
            
    def perform_sentiment_analysis(self, text):
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        self.text_display.insert(tk.END, f"\nSentiment: {sentiment}\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
