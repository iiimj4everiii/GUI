import os
import signal
import subprocess
from gui import *
from tkinter import *
import threading


class MainProcMgr:

    main_proc = None

    def __init__(self, main_script_path):
        self.main_script_path = main_script_path

    def spawn(self, test_plan_filename, bench_filename):
        test_plan_path = test_plan_filename
        bench_file_path = bench_filename
        return subprocess.Popen([self.main_script_path, "-b", bench_file_path, "-p", "-i", test_plan_path, "-u", "false"])


class ETCGUI(GUIProcess):

    def __init__(self, main_proc_mgr: MainProcMgr):
        super().__init__()

        self.setup_window("Telecaster", 800, 600)

        self.label = self.create_label(240, 50)
        self.label.set_label_text("Telecaster GUI", text_size=32, text_weight="bold")
        self.label.set_label_color((0, 0, 0), (0, 255, 0))

        self.main_proc_mgr = main_proc_mgr

        self.main_proc = None

        # working
        # gui_state = self.load_gui_state()

        self.tp_entry_label = self.create_label(100, 140)
        self.tp_entry_label.set_label_text("Test Plan", text_size=16, text_weight="bold")
        self.tp_entry_label.set_label_color((0, 0, 0), (0, 255, 0))
        self.tp_entry = self.create_entry(100, 175, 600)
        self.tp_entry.set_entry_color((0, 0, 0), (0, 255, 0))
        self.tp_entry.set_text_size(12)

        self.bench_entry_label = self.create_label(100, 240)
        self.bench_entry_label.set_label_text("Bench File", text_size=16, text_weight="bold")
        self.bench_entry_label.set_label_color((0, 0, 0), (0, 255, 0))
        self.bench_entry = self.create_entry(100, 275, 600)
        self.bench_entry.set_entry_color((0, 0, 0), (0, 255, 0))
        self.bench_entry.set_text_size(12)

        # main button
        self.main_button = self.create_button(50, 350, 200, 200)
        self.main_button.set_button_callback(self.main_button_click)
        self.reset_main_button()

        # abort button
        self.abort_button = self.create_button(550, 350, 200, 200)
        self.abort_button.set_button_callback(self.abort_button_click)
        self.abort_button.set_button_text("Abort", 16, "bold")
        self.abort_button.set_button_color((255, 0, 0), (0, 0, 0))

        # window exiting behavior
        self.window.protocol("WM_DELETE_WINDOW", self.on_exiting)

    def main_button_click(self):

        button_state = self.main_button.get_button_state()

        if self.main_proc is None:

            test_plan_filename = self.tp_entry.get_entry_text()
            if test_plan_filename[-4:] != ".csv":
                test_plan_filename += ".csv"

            bench_filename = self.bench_entry.get_entry_text()
            if bench_filename[-5:] != ".xlsx":
                bench_filename += ".xlsx"

            self.main_proc = self.main_proc_mgr.spawn(test_plan_filename, bench_filename)

            self.main_running()

            th = threading.Thread(target=self.polling)
            th.start()

        else:
            if button_state == "Run":
                os.kill(self.main_proc.pid, signal.SIGSTOP)
                self.main_pausing()

            else:
                os.kill(self.main_proc.pid, signal.SIGCONT)
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

    def save_gui_state(self):
        pass

    def load_gui_state(self):
        pass

    def on_exiting(self):
        # Abort any running tests before exiting the gui.
        self.abort_button_click()
        self.save_gui_state()
        self.window.destroy()


# MAIN_SCRIPT_PATH = "C:\\Users\\minjiang\\Documents\\Python\\gui\\main.py"
MAIN_SCRIPT_PATH = "/Applications/RFDATE/rfdate/Tester/RFTestPyMain.py"
main_proc_mgr = MainProcMgr(MAIN_SCRIPT_PATH)

G = ETCGUI(main_proc_mgr)

G.window.mainloop()
