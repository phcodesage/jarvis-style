import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pyaudio  # Used to get microphone list

# Function to recognize speech using Google Speech Recognition
def recognize_speech_from_mic(recognizer, microphone_index, text_var, error_var, listening_var, all_mics):
    # Select the microphone
    microphone = sr.Microphone(device_index=microphone_index)
    # Adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        listening_var.set("Listening...")  # Update the listening status
        text_var.set("")
        error_var.set("")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    listening_var.set("")  # Reset the listening status after recording

    # Try recognizing the speech in the recording
    try:
        transcription = recognizer.recognize_google(audio)
        text_var.set(transcription)
        error_var.set("")
    except sr.RequestError:
        error_var.set("API unavailable")
    except sr.UnknownValueError:
        error_var.set("Unable to recognize speech")

# This function will be used to start the speech recognition in a separate thread
def start_speech_recognition(mic_selection, text_var, error_var, listening_var, all_mics):
    recognizer = sr.Recognizer()
    mic_index = mic_selection.current()  # Get the index of the selected microphone
    speech_thread = Thread(target=recognize_speech_from_mic, args=(recognizer, mic_index, text_var, error_var, listening_var, all_mics))
    speech_thread.start()

# Get list of microphones
def get_microphone_list():
    mic_list = sr.Microphone.list_microphone_names()
    return mic_list

# Setting up the Tkinter GUI
def main():
    root = tk.Tk()
    root.title("Speech Recognition")
    root.geometry("500x300")  # Normal width and height

    # Make the window resizable
    root.resizable(True, True)  # Allow both horizontal and vertical resizing

    # Modern style
    style = ttk.Style(root)
    style.theme_use('clam')  # You can try different themes: 'alt', 'default', 'clam', 'classic'

    # Variables
    text_var = tk.StringVar()
    error_var = tk.StringVar()
    listening_var = tk.StringVar()

    # Microphone selection
    mic_label = ttk.Label(root, text="Select Microphone:")
    mic_label.pack(pady=(20, 5))
    all_mics = get_microphone_list()
    mic_selection = ttk.Combobox(root, values=all_mics, state="readonly")
    mic_selection.pack()
    mic_selection.current(0)  # Set to first microphone in list by default

    # Speech and error display
    ttk.Label(root, textvariable=text_var, wraplength=480).pack(pady=(20, 10))
    ttk.Label(root, textvariable=error_var, foreground="red", wraplength=480).pack()
    ttk.Label(root, textvariable=listening_var, foreground="blue", wraplength=480).pack(pady=(5, 20))

    # Start listening button
    ttk.Button(root, text="Start Listening", command=lambda: start_speech_recognition(mic_selection, text_var, error_var, listening_var, all_mics)).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
