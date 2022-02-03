import tkinter as tk
from tkinter import Label, Button, Tk, ttk
import tkinter.font as font
from color import Color


'''
Widgets     Description
Label	    It is used to display text or image on the screen
Button	    It is used to add buttons to your application
Canvas	    It is used to draw pictures and others layouts like texts, graphics etc.
ComboBox	It contains a down arrow to select from list of available options
CheckButton	It displays a number of options to the user as toggle buttons from which user can select any number of options.
RadiButton	It is used to implement one-of-many selection as it allows only one option to be selected
Entry	    It is used to input single line text entry from user
Frame	    It is used as container to hold and organize the widgets
Message	    It works same as that of label and refers to multi-line and non-editable text
Scale	    It is used to provide a graphical slider which allows to select any value from that scale
Scrollbar	It is used to scroll down the contents. It provides a slide controller.
SpinBox	    It is allows user to select from given set of values
Text	    It allows user to edit multiline text and format the way it has to be displayed
Menu	    It is used to create all kinds of menu used by an application
'''

'''
pack()	    The Pack geometry manager packs widgets in rows or columns.
grid()	    The Grid geometry manager puts the widgets in a 2-dimensional table. 
            The master widget is split into a number of rows and columns, and each “cell” in the
            resulting table can hold a widget.
place()	    The Place geometry manager is the simplest of the three general geometry managers provided
            in Tkinter. 
            It allows you explicitly set the position and size of a window, either in absolute terms,
            or relative to another window.
'''


class MyLabel:
    def __init__(self, window, x=0, y=0):
        self.label = Label(window)
        self.label.place(x=x, y=y)

    def set_label_text(self, label_text, text_size=10, text_weight="normal"):
        self.label.configure(text=label_text)
        self.label['font'] = font.Font(size=text_size, weight=text_weight)

    def set_label_color(self, background=(0, 0, 0), foreground=(0, 255, 0)):
        self.label.configure(background=Color.rgb_to_hex(background), foreground=Color.rgb_to_hex(foreground))


class MyButton:

    def __init__(self, window, x=0, y=0, width=100, height=100):
        self.state = "Ready"
        self.button = Button(window, text="button")
        self.button.place(x=x, y=y, width=width, height=height)

    def set_button_callback(self, callback):
        self.button.configure(command=callback)

    def set_button_text(self, button_text, text_size=10, text_weight="normal"):
        self.button.configure(text=button_text)
        self.button['font'] = font.Font(size=text_size, weight=text_weight)

    def set_button_color(self, background=(0, 0, 0), foreground=(0, 255, 0)):
        self.button.configure(background=Color.rgb_to_hex(background), activebackground=Color.rgb_to_hex(background),
                              foreground=Color.rgb_to_hex(foreground), activeforeground=Color.rgb_to_hex(foreground))

    def set_button_state(self, state):
        self.state = state

    def get_button_state(self):
        return self.state


class MyEntry:

    def __init__(self, window, x=0, y=0, width=100):
        self.entry_text = tk.StringVar()
        self.entry = ttk.Entry(window, textvariable=self.entry_text)
        self.entry.place(x=x, y=y, width=width)

    def set_text_size(self, text_size=10):
        self.entry.configure(font="Courier {text_size}".format(text_size=text_size))

    def set_entry_color(self, background=(0, 0, 0), foreground=(0, 255, 0)):
        style = ttk.Style()
        style.configure("style.TEntry", background=Color.rgb_to_hex(background), foreground=Color.rgb_to_hex(foreground))
        self.entry.configure(style="style.TEntry")

    def get_entry_text(self):
        return self.entry.get()


class GUIProcess:

    def __init__(self):
        self.window = Tk()
        self.window.configure(bg=Color.rgb_to_hex((0, 0, 0)))

        self.window.bind("<Return>", self.on_return)

    def setup_window(self, title="GUI", width=500, height=500):
        self.window.title(title)
        self.window.geometry("{0}x{1}".format(width, height))

    def create_label(self, x=0, y=0):
        return MyLabel(self.window, x=x, y=y)

    def create_button(self, x=0, y=0, width=100, height=100):
        return MyButton(self.window, x=x, y=y, width=width, height=height)

    def create_entry(self, x=0, y=0, width=100):
        return MyEntry(self.window, x=x, y=y, width=width)

    # Used to remove focus (blinking cursors) away from text boxes after pressing the ENTER key.
    # Python question: where does the argument event come from?
    # It is not explicitly passed in the code: self.window.bind("<Key>", self.on_return)
    def on_return(self, event):
        if event.keysym == "Return":
            self.window.focus_set()
