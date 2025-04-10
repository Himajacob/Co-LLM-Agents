import tkinter as tk
from gtts import gTTS
import pyttsx3
import os
import pygame
import time
import re
import threading

# Initialize pygame mixer
pygame.mixer.init()

# Initialize pyttsx3 engine for Bob
engine = pyttsx3.init()
engine.setProperty('rate', 150)    # Adjust speaking rate for clarity
engine.setProperty('volume', 1.0)    # Max volume

# Attempt to select a male voice
for voice in engine.getProperty('voices'):
    if 'male' in voice.name.lower() or 'en' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

# File and separator
chat_file = 'conversation_log.txt'
separator = '-------------------------------------------------------------------------------------'
running = True  # Global flag to control chat playback

# Function to clean text by removing <, >, and " symbols (and smart quotes)
def clean_text(text):
    return re.sub(r'[<>"“”]', '', text).strip()

# Alice's TTS using gTTS (female voice, Australian accent)
def play_tts_alice(text):
    tts = gTTS(text=text, lang='en', tld='com.au')
    audio_file = "alice_temp.mp3"
    tts.save(audio_file)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        root.update()
        time.sleep(0.1)
    # Stop and unload to free file lock
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove(audio_file)

# Bob's TTS using pyttsx3 (male voice)
def play_tts_bob(text):
    audio_file = "bob_temp.wav"
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        root.update()
        time.sleep(0.1)
    # Stop and unload to free file lock
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove(audio_file)

# Create a chat bubble with increased horizontal spacing
def create_bubble(text, side, color):
    bubble_frame = tk.Frame(chat_frame, bg="white")
    bubble = tk.Label(
        bubble_frame,
        text=text,
        bg=color,
        fg="black",
        font=("Helvetica", 12),
        padx=15,
        pady=10,
        wraplength=400,
        justify='left',
        anchor='w'
    )
    bubble.pack(pady=5, padx=5)
    # Increase horizontal space between bubbles
    if side == 'w':
        bubble_frame.pack(anchor=side, padx=(30, 100), pady=5)
    else:
        bubble_frame.pack(anchor=side, padx=(100, 30), pady=5)

# Display chat bubble and play corresponding audio
def play_and_display(speaker, text):
    text = clean_text(text)
    if not text or not running:
        return
    if speaker == 'Alice':
        create_bubble(f"Alice:\n{text}", 'w', "#DCF8C6")
        root.update()
        play_tts_alice(text)
    else:
        create_bubble(f"Bob:\n{text}", 'e', "#ADD8E6")
        root.update()
        play_tts_bob(text)

# Load conversation from file
def load_conversation():
    with open(chat_file, 'r', encoding='utf-8') as file:
        content = file.read()
    conversations = content.split(separator)
    dialog_list = []
    for convo in conversations:
        convo = convo.strip()
        if convo:
            if convo.startswith('Alice:'):
                dialog_list.append(('Alice', convo.replace('Alice:', '').strip()))
            elif convo.startswith('Bob:'):
                dialog_list.append(('Bob', convo.replace('Bob:', '').strip()))
    return dialog_list

# Run the chat in a separate thread
# def run_chat():
#     global running
#     running = True
#     dialog_list = load_conversation()
#     for speaker, text in dialog_list:
#         if not running:
#             break
#         play_and_display(speaker, text)
#     canvas.yview_moveto(1)

def run_chat():
    global running
    running = True

    with open(chat_file, 'r', encoding='utf-8') as file:
        buffer = []
        while running:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue

            if line.strip() == separator:
                # End of one full conversation block — process it now
                dialog_list = []
                for entry in buffer:
                    if entry.startswith('Alice:'):
                        dialog_list.append(('Alice', entry.replace('Alice:', '').strip()))
                    elif entry.startswith('Bob:'):
                        dialog_list.append(('Bob', entry.replace('Bob:', '').strip()))

                for speaker, text in dialog_list:
                    if not running:
                        break
                    play_and_display(speaker, text)

                buffer.clear()

                if running:
                    time.sleep(10)  # ⏳ Pause between full conversation blocks

            else:
                buffer.append(line.strip())

    canvas.yview_moveto(1)



def start_chat():
    threading.Thread(target=run_chat).start()

def stop_chat():
    global running
    running = False
    pygame.mixer.music.stop()

# Set up the main GUI window
root = tk.Tk()
root.title("Alice and Bob Chat")
root.geometry("900x700")

# Create chat container with a scrollbar (only for the chat area)
chat_container = tk.Frame(root, bg="white")
chat_container.pack(side="top", fill="both", expand=True)

canvas = tk.Canvas(chat_container, bg="white")
scrollbar = tk.Scrollbar(chat_container, command=canvas.yview)
chat_frame = tk.Frame(canvas, bg="white")

chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=chat_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Button frame at the bottom of the window
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

# Circular styled Start Button (green with drop shadow effect simulated)
start_button = tk.Button(
    button_frame, text="Start", command=start_chat, font=("Helvetica", 14),
    bg="#4CAF50", fg="white", bd=0, relief="flat",
    activebackground="#45a049", width=6, height=2, cursor="hand2"
)
start_button.pack(side="left", padx=20)

# Circular styled Stop Button (red)
stop_button = tk.Button(
    button_frame, text="Stop", command=stop_chat, font=("Helvetica", 14),
    bg="#f44336", fg="white", bd=0, relief="flat",
    activebackground="#c0392b", width=6, height=2, cursor="hand2"
)
stop_button.pack(side="left", padx=20)

root.mainloop()
