from tkinter import *
import tkinter.font as font
from color import Color


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


class GUIProcess:

    def __init__(self):
        self.window = Tk()
        self.window.configure(bg=Color.rgb_to_hex((0, 0, 0)))

    def setup_window(self, title="GUI", width=500, height=500):
        self.window.title(title)
        self.window.geometry("{0}x{1}".format(width, height))

    def create_button(self, x=0, y=0, width=100, height=100):
        return MyButton(self.window, x=x, y=y, width=width, height=height)
