from gui import *
from helpers import *
import os
import signal
import subprocess
import threading


class MainProcMgr:

    main_proc = None

    def __init__(self, main_script_path, test_plan_file_dir, bench_file_dir):

        self.main_script_path = main_script_path

        self.test_plan_file_dir = check_and_fix_dir_path(test_plan_file_dir)

        self.bench_file_dir = check_and_fix_dir_path(bench_file_dir)

    def spawn(self, test_plan_filename, bench_filename):

        python_version = get_python_version()
        test_plan_path = self.test_plan_file_dir + test_plan_filename
        bench_file_path = self.bench_file_dir + bench_filename

        return subprocess.Popen([python_version, self.main_script_path, "-b", bench_file_path, "-p", "-i",
                                 test_plan_path, "-u", "false"])


class ETCGUI(GUIProcess):

    def __init__(self, main_proc_mgr: MainProcMgr):
        super().__init__()

        self.setup_window("Telecaster", 800, 600)

        self.label = self.create_label(280, 50)
        self.label.set_label_text("Telecaster GUI", text_size=32, text_weight="bold")
        self.label.set_label_color((0, 0, 0), (0, 255, 0))

        self.main_proc_mgr = main_proc_mgr

        self.main_proc = None

        self.tp_entry_label = self.create_label(100, 150)
        self.tp_entry_label.set_label_text("Test Plan:", text_size=16, text_weight="bold")
        self.tp_entry_label.set_label_color((0, 0, 0), (0, 255, 0))

        self.tp_entry = self.create_entry(100, 175, 600)
        self.tp_entry.set_entry_color((0, 0, 0), (0, 255, 0))
        self.tp_entry.set_text_size(14)

        self.bench_entry_label = self.create_label(100, 250)
        self.bench_entry_label.set_label_text("Bench File:", text_size=16, text_weight="bold")
        self.bench_entry_label.set_label_color((0, 0, 0), (0, 255, 0))

        self.bench_entry = self.create_entry(100, 275, 600)
        self.bench_entry.set_entry_color((0, 0, 0), (0, 255, 0))
        self.bench_entry.set_text_size(14)

        # abort button
        self.abort_button = self.create_button(550, 350, 200, 200)
        self.abort_button.set_button_callback(self.abort_button_click)
        self.abort_button.set_button_text("Abort", 24, "bold")
        self.abort_button.set_button_color((255, 255, 255), (255, 0, 0))

        # main button
        self.main_button = self.create_button(50, 350, 200, 200)
        self.main_button.set_button_callback(self.main_button_click)

        self.reset_gui_state()

        # window exiting behavior
        self.window.protocol("WM_DELETE_WINDOW", self.on_exiting)

        self.load_gui_state()

    def main_button_click(self):

        if self.main_proc is None:

            test_plan_filename = check_and_fix_file_extension(self.tp_entry.get_entry_text(), "csv")

            bench_filename = check_and_fix_file_extension(self.bench_entry.get_entry_text(), "xlsx")

            self.main_proc = self.main_proc_mgr.spawn(test_plan_filename, bench_filename)

            self.tp_entry.disable()
            self.bench_entry.disable()
            self.main_running()

            th_run_main = threading.Thread(target=self.main_proc_polling)
            th_run_main.start()

        else:
            button_state = self.main_button.get_button_state()

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
            self.reset_gui_state()

    def main_pausing(self):
        self.main_button.set_button_text("Resume", 24, "bold")
        self.main_button.set_button_color((255, 255, 255), (0, 0, 0))

        self.main_button.set_button_state("Paused")

    def main_running(self):
        self.main_button.set_button_text("Pause", 24, "bold")
        self.main_button.set_button_color((255, 255, 255), (255, 0, 0))

        self.main_button.set_button_state("Run")

    def reset_gui_state(self):
        self.main_button.set_button_state("Ready")
        self.main_button.set_button_text("Run", 24, "bold")
        self.main_button.set_button_color((255, 255, 255), (0, 0, 0))

        self.tp_entry.enable()
        self.bench_entry.enable()

    def main_proc_polling(self):
        while True:
            if self.main_proc is None:
                return

            if self.main_proc.poll() is not None:
                self.main_proc = None
                self.reset_gui_state()
                return

    def save_gui_state(self):
        gui_state = {
            "tp_entry":     self.tp_entry.get_entry_text(),
            "bench_entry":  self.bench_entry.get_entry_text()
        }

        write_dict_to_json_file(gui_state, "gui_state")

    def load_gui_state(self):
        gui_state = read_json_file_to_dict("gui_state.json")

        self.tp_entry.set_entry_text(gui_state["tp_entry"])
        self.bench_entry.set_entry_text(gui_state["bench_entry"])

    def on_exiting(self):
        # Abort any running tests before exiting the gui.
        self.save_gui_state()
        self.abort_button_click()
        self.window.destroy()


# MAIN_SCRIPT_PATH = "C:\\Users\\minjiang\\Documents\\Python\\gui\\main.py"
settings = read_json_file_to_dict("Path_Settings.json")
main_proc_mgr = MainProcMgr(settings["main_script_path"], settings["test_plan_file dir"], settings["bench_file_dir"])

G = ETCGUI(main_proc_mgr)

G.window.mainloop()
