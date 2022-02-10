from helpers import *
import threading
import signal


class TCGUIEventHandler:
    def __init__(self, tc_gui):
        self.tc_gui = tc_gui

    def main_button_click(self):

        if self.tc_gui.main_proc is None:

            self.tc_gui.dut = self.tc_gui.DUT_entry.get_entry_text().strip()

            if self.tc_gui.check_magic(self.tc_gui.dut):
                return

            test_plan_filename = check_and_fix_file_extension(self.tc_gui.tp_entry.get_entry_text(), "csv")

            bench_filename = check_and_fix_file_extension(self.tc_gui.bench_entry.get_entry_text(), "xlsx")

            self.tc_gui.main_proc = self.tc_gui.main_proc_mgr.spawn(self.tc_gui.dut, test_plan_filename, bench_filename)

            self.tc_gui.DUT_entry.disable()
            self.tc_gui.comment_entry.disable()
            self.tc_gui.tp_entry.disable()
            self.tc_gui.bench_entry.disable()

            self.main_running()

            th_run_main = threading.Thread(target=self.tc_gui.main_proc_polling)
            th_run_main.start()

        else:
            button_state = self.tc_gui.main_button.get_button_state()

            if button_state == "Run":
                os.kill(self.tc_gui.main_proc.pid, signal.SIGSTOP)
                self.main_pausing()

            else:
                os.kill(self.tc_gui.main_proc.pid, signal.SIGCONT)
                self.main_running()

    def abort_button_click(self):
        if self.tc_gui.main_proc is not None:
            os.kill(self.tc_gui.main_proc.pid, signal.SIGTERM)
            self.tc_gui.main_proc = None
            self.reset_gui_state()

    def main_pausing(self):
        self.tc_gui.main_button.set_button_text("Resume", 24, "bold")
        self.tc_gui.main_button.set_button_color((255, 255, 255), (0, 0, 0))

        self.tc_gui.main_button.set_button_state("Paused")

    def main_running(self):
        self.tc_gui.main_button.set_button_text("Pause", 24, "bold")
        self.tc_gui.main_button.set_button_color((255, 255, 255), (255, 0, 0))

        self.tc_gui.main_button.set_button_state("Run")

    def reset_gui_state(self):
        self.tc_gui.main_button.set_button_state("Ready")
        self.tc_gui.main_button.set_button_text("Run", 24, "bold")
        self.tc_gui.main_button.set_button_color((255, 255, 255), (0, 0, 0))

        self.tc_gui.DUT_entry.enable()
        self.tc_gui.comment_entry.enable()
        self.tc_gui.tp_entry.enable()
        self.tc_gui.bench_entry.enable()

    def save_gui_state(self):
        gui_state = {
            "dut_entry":        self.tc_gui.DUT_entry.get_entry_text(),
            "comment_entry":    self.tc_gui.comment_entry.get_entry_text(),
            "tp_entry":         self.tc_gui.tp_entry.get_entry_text(),
            "bench_entry":      self.tc_gui.bench_entry.get_entry_text()
        }

        write_dict_to_json_file(gui_state, os.path.join(self.tc_gui.main_proc_mgr.gui_program_dir, "gui_state"))

    def load_gui_state(self):
        gui_state = read_json_file_to_dict(os.path.join(self.tc_gui.main_proc_mgr.gui_program_dir, "gui_state.json"))

        self.tc_gui.DUT_entry.set_entry_text(gui_state["dut_entry"])
        self.tc_gui.comment_entry.set_entry_text(gui_state["comment_entry"])
        self.tc_gui.tp_entry.set_entry_text(gui_state["tp_entry"])
        self.tc_gui.bench_entry.set_entry_text(gui_state["bench_entry"])

        path_settings_path = os.path.join(self.tc_gui.main_proc_mgr.gui_program_dir, "Path_Settings")
        path_settings = read_json_file_to_dict(path_settings_path + ".json")
        if path_settings["magic"] == "on":
            self.tc_gui.title_label.set_label_color((0, 0, 0), (255, 0, 0))
