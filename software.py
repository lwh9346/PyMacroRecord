import threading
from tkinter import *
from tkinter.ttk import *
from pynput import keyboard
import subprocess
import atexit
import os
import signal
import time

keyboardControl = keyboard.Controller()

def cleanup():
    if 'macro_process' in globals():
        macro_process.terminate()

atexit.register(cleanup)

macro_process = subprocess.Popen(['python', 'macro.py'])

# Window Setup
window = Tk()
window.title("MacroRecorder")
window.geometry("350x200")
window.iconbitmap("assets/logo.ico")

my_menu = Menu(window)
window.config(menu=my_menu)


def startRecordingAndChangeImg():
    global stopBtn
    global lenghtOfRecord
    recordBtn.pack_forget()
    stopBtn.pack(side=RIGHT, padx=50)
    keyboardControl.press('1')
    keyboardControl.release('1')
    lenghtOfRecord = time.time()

def stopRecordingAndChangeImg():
    global recordBtn
    global lenghtOfRecord
    stopBtn.pack_forget()
    recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
    recordBtn.pack(side=RIGHT, padx=50)
    keyboardControl.press('2')
    keyboardControl.release('2')
    lenghtOfRecord = (time.time() - lenghtOfRecord) + 0.5

def replay():
    recordBtn.configure(state=DISABLED)
    keyboardControl.press('3')
    keyboardControl.release('3')
    threading.Thread(target=buttonDisabledToEnable).start()

def buttonDisabledToEnable():
    time.sleep(lenghtOfRecord)
    recordBtn.configure(state=NORMAL)


# Menu Bar
file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Save", command=window.quit, state=DISABLED)
file_menu.add_command(label="Save as", command=window.quit, state=DISABLED)
file_menu.add_separator()
file_menu.add_command(label="Settings", command=window.quit)

# Play Button
playImg = PhotoImage(file=r"assets/button/play.png")
playBtn = Button(window, image=playImg, command=replay)
playBtn.pack(side=LEFT, padx=50)

# Record Button
recordImg = PhotoImage(file=r"assets/button/record.png")
recordBtn = Button(window, image=recordImg, command=startRecordingAndChangeImg)
recordBtn.pack(side=RIGHT, padx=50)

# Stop Button
stopImg = PhotoImage(file=r"assets/button/stop.png")
stopBtn = Button(window, image=stopImg, command=stopRecordingAndChangeImg)


window.mainloop()