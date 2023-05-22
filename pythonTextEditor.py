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


def darkTitleBar(window):
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
    global filename
    global currentSave
    filename = fd.askopenfilename()
    words = ""
    if filename != "":
        newFile()
        with open(filename) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                words += line
            window.title("Text Editor " + "~ " + filename)
            textWidget.insert(INSERT, words)
            currentSave = words


def saveFile(self):
    global filename
    global currentSave
    newpath = userpaths.get_my_documents() + "\\PythonTextEditor\\"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    if filename != "" and filename is not None:
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
            if answer != ".txt" and answer is not None:
                try:
                    filename = answer
                    currentSave = textWidget.get("1.0", "end-1c")
                except:
                    pass
                break
            else:
                break

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


def onClose():
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


def createNewFile():
    global filename
    global currentSave
    newpath = userpaths.get_my_documents() + "\\PythonTextEditor\\"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    while True:
        answer = ""
        answer = simpledialog.askstring(
            "Input", "Enter a valid filename", parent=window, initialvalue=".txt"
        )
        if answer != ".txt" and answer is not None:
            try:
                filename = answer
                currentSave = textWidget.get("1.0", "end-1c")
            except:
                pass
            break
        else:
            break
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


menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New File", command=createNewFile)
filemenu.add_command(label="Clear", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=lambda: saveFile(None))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=onClose)
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
darkTitleBar(window)
window.title("Text Editor")
window.geometry("500x500")
window.config(menu=menubar)
window.protocol("WM_DELETE_WINDOW", onClose)
window.iconbitmap("myIcon.ico")
window.bind("<Control-s>", saveFile)
window.mainloop()
