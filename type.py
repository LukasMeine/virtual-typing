import tkinter as tk
from tkinter import ttk
import pyautogui
import random
import time
from threading import Thread

class TypingEngine:
    def __init__(self, min_delay=0, max_delay=0, typo_frequency=0.02):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.typo_frequency = typo_frequency  # Chance of a typo happening

    def set_min_delay(self, min_delay):
        self.min_delay = min_delay

    def set_max_delay(self, max_delay):
        self.max_delay = max_delay

    def typing_forward(self, final_form):
        i = 0
        while i < len(final_form) and is_running:
            time.sleep(self.get_random_number(self.min_delay, self.max_delay))

            # Chance to make a typo
            if random.random() < self.typo_frequency:
                typo_char = self.get_random_typo(final_form[i])
                pyautogui.write(typo_char)  # Writes the wrong character
                time.sleep(self.get_random_number(self.min_delay, self.max_delay))
                pyautogui.hotkey('backspace')  # Deletes the wrong character
                time.sleep(self.get_random_number(self.min_delay, self.max_delay))

            pyautogui.write(final_form[i])  # Writes the correct character

            # Pause after a period
            if final_form[i] == '.':
                time.sleep(1)

            i += 1
        start_button.config(state="enabled")  
        stop_button.config(state="disabled") 
        

    def get_random_number(self, min_val, max_val):
        return random.uniform(min_val, max_val)

    def get_random_typo(self, correct_char):
        # Dictionary with typo possibilities
        typo_dict = {
            'a': 's', 'b': 'v', 'c': 'x', 'd': 's', 'e': 'w', 'f': 'd', 'g': 'f', 'h': 'g',
            'i': 'o', 'j': 'h', 'k': 'j', 'l': 'k', 'm': 'n', 'n': 'b', 'o': 'p', 'p': 'o',
            'q': 'w', 'r': 't', 's': 'a', 't': 'r', 'u': 'y', 'v': 'c', 'w': 'q', 'x': 'z',
            'y': 'u', 'z': 'x', '1': '2', '2': '3', '3': '4', '4': '5', '5': '6', '6': '7',
            '7': '8', '8': '9', '9': '0', '0': '9', ',': '.', '.': ',', '/': '.', ' ': 'v'
        }
        return typo_dict.get(correct_char, correct_char)

engine = TypingEngine(min_delay=0.001, max_delay=0.008)
is_running = False

def start_typing():
    global is_running
    is_running = True
    start_button.config(state="disabled")  # Enable the start button
    stop_button.config(state="enabled")  # Disable the stop button
    delay = delay_scale.get()
    text = text_entry.get("1.0", "end-1c")  # Get text from text entry widget
    if delay > 0:
        status_label.config(text=f"Starting in {delay} seconds..")
        root.after(1000, update_countdown, delay, text)  # Start countdown before typing
    else:
        status_label.config(text="Running..")
        Thread(target=typing_thread, args=(text,)).start()  # Start typing in a separate thread

def typing_thread(text):
    engine.typing_forward(text)
    if is_running:  # Check if not stopped by the stop button
        status_label.config(text="Finished")

def update_countdown(delay, text):
    global is_running
    if delay > 0 and is_running:
        delay -= 1
        status_label.config(text=f"Starting in {delay} seconds..")
        root.after(1000, update_countdown, delay, text)
    elif is_running:
        status_label.config(text="Running..")
        Thread(target=typing_thread, args=(text,)).start()  # Start typing in a separate thread

def stop_typing():
    global is_running
    is_running = False
    start_button.config(state="enabled")  
    stop_button.config(state="disabled")  
    status_label.config(text="Stopped")

def update_slider(*args):
    text_entry.edit_modified(False)  # Reset the modified flag
    #delay_scale.set(0)  # Set the slider to 0 when text changes

root = tk.Tk()
root.title("virtual typing")
root.geometry("435x420")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

text_label = ttk.Label(mainframe, text="Text to type:")
text_label.grid(column=0, row=0, padx=5, pady=5)

text_entry = tk.Text(mainframe, height=10, width=50)
text_entry.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.E))
text_entry.bind("<<Modified>>", update_slider)

delay_label = ttk.Label(mainframe, text="Delay before start typing (in seconds):")
delay_label.grid(column=0, row=2, padx=5, pady=5)

delay_scale = ttk.Scale(mainframe, from_=0, to=5, orient='horizontal')
delay_scale.grid(column=0, row=3, padx=5, pady=5)

status_label = ttk.Label(mainframe, text="Waiting for user input")
status_label.grid(column=0, row=4, padx=5, pady=5)

start_button = ttk.Button(mainframe, text="Start", command=start_typing)
start_button.grid(column=0, row=5, padx=5, pady=5)

stop_button = ttk.Button(mainframe, text="Stop", command=stop_typing)
stop_button.grid(column=0, row=6, padx=5, pady=5)

root.mainloop()
