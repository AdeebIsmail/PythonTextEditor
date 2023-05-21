from tkinter import *
import ctypes as ct
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import simpledialog
import webbrowser
import userpaths
import os

window = Tk()
window.geometry("500x500")

filename = ""
currentSave = ""


def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


def wordCount():
    text = textWidget.get("1.0", "end-1c")
    count = 0
    lastWord = ""
    for i in text:
        if i == " " and lastWord != " ":
            count += 1
        lastWord = i
    content = textWidget.get("1.0", "end-1c")
    if lastWord != " ":
        count += 1
    if content.isspace() or content == "":
        count = 0
    messagebox.showinfo("Word Count", "You have " + str(count) + " words")


def characterCount():
    text = textWidget.get("1.0", "end-1c")
    count = 0
    for i in text:
        if i != " ":
            count += 1
    messagebox.showinfo("Character Count", "You have " + str(count) + " characters")


def newFile():
    textWidget.delete("1.0", "end-1c")


def openFile():
    newFile()
    global filename
    global currentSave
    filename = fd.askopenfilename()
    words = ""
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            words += line
    window.title("Text Editor " + "~ " + filename)
    textWidget.insert(INSERT, words)
    currentSave = words


def saveFile():
    global filename
    global currentSave

    newpath = userpaths.get_my_documents() + "\\PythonTextEditor\\"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    if filename != "":
        text = textWidget.get("1.0", "end-1c")
        words = ""
        for i in text:
            words += i
        file = open(filename, "w")
        file.write(words)
        window.title("Text Editor " + "~ " + filename)
        currentSave = textWidget.get("1.0", "end-1c")
        file.close()
    else:
        while True:
            answer = ""
            answer = simpledialog.askstring(
                "Input", "Enter a valid filename", parent=window, initialvalue=".txt"
            )
            if answer != "":
                try:
                    filename = answer + ".txt"
                    currentSave = textWidget.get("1.0", "end-1c")
                except:
                    pass
                break
            else:
                print("Dawg what")

        try:
            text = textWidget.get("1.0", "end-1c")
            words = ""
            for i in text:
                words += i
            file = open(
                userpaths.get_my_documents() + "\\PythonTextEditor\\" + filename, "w"
            )
            filename = userpaths.get_my_documents() + "\\PythonTextEditor\\" + filename
            file.write(words)
            window.title("Text Editor " + "~ " + filename)
            file.close()
        except:
            pass


def about():
    webbrowser.open("https://github.com/AdeebIsmail/PythonTextEditor")


def on_close():
    if currentSave != textWidget.get("1.0", "end-1c"):
        res = messagebox.askquestion(
            "Warning",
            "Are you sure you want to quit? Anything not saved will be lost.",
            default="no",
        )
        if res == "yes":
            window.destroy()
        else:
            pass
    else:
        window.destroy()


menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_close)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

toolmenu = Menu(menubar, tearoff=0)
toolmenu.add_command(label="Word Count", command=wordCount)
toolmenu.add_command(label="Character Count", command=characterCount)
menubar.add_cascade(label="Tools", menu=toolmenu)

textWidget = Text(window)
textWidget.pack(expand=True, fill="both")
dark_title_bar(window)
window.title("Text Editor")
window.geometry("500x500")
window.config(menu=menubar)
window.protocol("WM_DELETE_WINDOW", on_close)
window.iconbitmap("myIcon.ico")
window.mainloop()
