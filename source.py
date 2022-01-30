import os
import signal
import subprocess
from gui import *
import threading


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


class MainProcMgr:

    main_proc = None

    def __init__(self, main_script_path):
        self.main_script_path = main_script_path

    def spawn(self):
        return subprocess.Popen([sys.executable, self.main_script_path])


class ETCGUI(GUIProcess):

    def __init__(self, main_proc_mgr: MainProcMgr):
        super().__init__()

        self.setup_window("Telecaster", 500, 200)

        self.main_proc_mgr = main_proc_mgr

        self.main_proc = None

        # main button
        self.main_button = self.create_button(0, 0, 200, 200)
        self.main_button.set_button_callback(self.main_button_click)
        self.reset_main_button()

        # abort button
        self.abort_button = self.create_button(300, 0, 200, 200)
        self.abort_button.set_button_callback(self.abort_button_click)
        self.abort_button.set_button_text("Abort", 16, "bold")
        self.abort_button.set_button_color((255, 0, 0), (0, 0, 0))

        # window exiting behavior
        self.window.protocol("WM_DELETE_WINDOW", self.on_exiting)

    def main_button_click(self):

        button_state = self.main_button.get_button_state()

        if self.main_proc is None:
            self.main_proc = self.main_proc_mgr.spawn()

            self.main_running()

            th = threading.Thread(target=self.polling)
            th.start()

        else:
            if button_state == "Run":
                # os.kill(self.main_proc.pid, signal.SIGSTOP)
                self.main_pausing()

            else:
                # os.kill(self.main_proc.pid, signal.SIGCONT)
                self.main_running()

    def abort_button_click(self):
        if self.main_proc is not None:
            os.kill(self.main_proc.pid, signal.SIGTERM)
            self.main_proc = None
            self.reset_main_button()

    def main_pausing(self):
        self.main_button.set_button_text("RESUME", 16, "bold")
        self.main_button.set_button_color((0, 0, 0), (0, 255, 0))
        self.main_button.set_button_state("Paused")

    def main_running(self):
        self.main_button.set_button_text("PAUSE", 16, "bold")
        self.main_button.set_button_color((255, 0, 0), (0, 0, 0))
        self.main_button.set_button_state("Run")

    def reset_main_button(self):
        self.main_button.set_button_state("Ready")
        self.main_button.set_button_text("Run", 16, "bold")
        self.main_button.set_button_color((0, 0, 0), (0, 255, 0))

    def polling(self):
        while True:
            if self.main_proc is None:
                return

            if self.main_proc.poll() is not None:
                self.main_proc = None
                self.reset_main_button()
                return

    def on_exiting(self):
        self.abort_button_click()
        self.window.destroy()


MAIN_SCRIPT_PATH = "C:\\Users\\minjiang\\Documents\\Python\\gui\\main.py"
main_proc_mgr = MainProcMgr(MAIN_SCRIPT_PATH)

G = ETCGUI(main_proc_mgr)

G.window.mainloop()
