from SizeAndShapeDetection import mainfunction
import tkinter.filedialog as filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog
import filetype
import os.path
from os import path
  
# Make a regular expression for 
# identifying Floating point number  
master = tk.Tk()

def answer():
    mb.showerror("Error", "Wrong file path or wrong file extention")

def answer1():
    mb.showerror("Error", "Wrong input. Please enter only number")

def inputFunction():
    input_path = tk.filedialog.askopenfilename(defaultextension=".jpeg", 
                                      filetypes=[("All Files","*.*"), 
                                        ("Image File","*.png")])
    input_entry.insert(0, input_path)  # Insert the 'path'

def outputFunction():
    output_path = tk.filedialog.askdirectory()
    output_entry.insert(0, output_path)  # Insert the 'path'

def helloCallBack(filePathDict):
    validextension = ['jpg','png','jpeg']
    inputPath = input_entry.get()
    try:
        if len(inputPath.strip()) == 0:
            answer()
            return
        kind = filetype.guess(inputPath)
        kindtype = str(kind.extension)
        if kindtype not in validextension:
            answer()
            return
    except FileNotFoundError:
        answer()
        return

    outputPath = output_entry.get()
    try:
        if path.isdir(outputPath) == False:
            answer()
            return
    except FileNotFoundError:
        answer()
        return
    
    pixelPerCM = e1.get()
        
    try:
        pixelPerCM = float(pixelPerCM)
    except ValueError:
        answer1()
        return
    
    filePathDict['inputPath'] = inputPath
    filePathDict['outputPath'] = outputPath
    filePathDict['pixelPerCM'] = pixelPerCM
    print(filePathDict)
    mainfunction(filePathDict)

top_frame = tk.Frame(master)
bottom_frame = tk.Frame(master)
line = tk.Frame(master, height=1, width=400, bg="grey80", relief='groove')
filePathDict = {}

input_path = tk.Label(top_frame, text="Input File Path:")
input_entry = tk.Entry(top_frame, width=40)
browse1 = tk.Button(top_frame, text="Browse", command = inputFunction)

e1_entry = tk.Label(top_frame, text="Pixel Per Centimeter:")
e1 = tk.Entry(top_frame,text="",width=20)


output_path = tk.Label(bottom_frame, text="Output File Path:")
output_entry = tk.Entry(bottom_frame, text="", width=40)
browse2 = tk.Button(bottom_frame, text="Browse", command= outputFunction)

begin_button = ttk.Button(bottom_frame, text='Start', command= lambda: helloCallBack(filePathDict))

top_frame.pack(side=tk.TOP)
line.pack(pady=10)
bottom_frame.pack(side=tk.BOTTOM)

input_path.pack(pady=5)
input_entry.pack(pady=5)
browse1.pack(pady=5)

e1_entry.pack(pady=5)
e1.pack(pady=5)

output_path.pack(pady=5)
output_entry.pack(pady=5)
browse2.pack(pady=5)

begin_button.pack(pady=20)
master.title("SS PROJECT")

master.mainloop()
