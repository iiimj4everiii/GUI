from main_proc_manager import MainProcMgr
from gui import GUIProcess
from tc_gui_widget_event_handler import TCGUIWidgetEventHandler
from helpers import *


class TCGUI(GUIProcess):

    def __init__(self, main_proc_mgr: MainProcMgr):
        super().__init__()

        self.dut = ""

        self.output_file_path = ""

        self.extra_folder_name = ""

        self.setup_window("Telecaster", 900, 700)

        self.title_label = self.create_label(335, 50)
        self.title_label.set_label_text("Telecaster GUI", text_size=32, text_weight="bold")
        self.title_label.set_label_color((0, 0, 0), (0, 255, 0))

        self.main_proc_mgr = main_proc_mgr

        self.main_proc = None

        self.DUT_entry = self.Telecaster_entry(50, 150, "DUT:", 125, 150, 725)

        self.comment_entry = self.Telecaster_entry(50, 225, "Comment:", 175, 225, 675)

        self.tp_entry = self.Telecaster_entry(50, 300, "Test Plan:", 175, 300, 675)

        self.bench_entry = self.Telecaster_entry(50, 375, "Bench File:", 175, 375, 675)

        # abort button
        self.abort_button = self.create_button(650, 450, 200, 200)
        self.abort_button.set_button_text("Abort", 24, "bold")
        self.abort_button.set_button_color((255, 255, 255), (255, 0, 0))

        # main button
        self.main_button = self.create_button(50, 450, 200, 200)

        self.event_handler = TCGUIWidgetEventHandler(self)

        self.abort_button.set_button_callback(self.event_handler.abort_button_click)
        self.main_button.set_button_callback(self.event_handler.main_button_click)

        self.event_handler.reset_gui_state()
        self.event_handler.load_gui_state()

        # window exiting behavior
        self.window.protocol("WM_DELETE_WINDOW", self.on_exiting)

    def Telecaster_entry(self, label_x, label_y, label_text, entry_x, entry_y, entry_width):

        label = self.create_label(label_x, label_y)
        label.set_label_text(label_text, text_size=18, text_weight="bold")
        label.set_label_color((0, 0, 0), (0, 255, 0))

        entry = self.create_entry(entry_x, entry_y, entry_width)
        entry.set_entry_color((0, 0, 0), (0, 255, 0))
        entry.set_text_size(16)

        return entry

    def main_proc_polling(self):
        while True:
            if self.main_proc is None:
                return

            if self.main_proc.poll() is not None:
                self.main_proc = None
                self.event_handler.reset_gui_state()

                comment = self.comment_entry.get_entry_text().strip()
                if comment != "":
                    result_dir = os.path.join(self.main_proc_mgr.result_parent_dir, self.dut)
                    os.rename(src=os.path.join(result_dir, self.extra_folder_name),
                              dst=os.path.join(result_dir, comment))

                return

            main_proc_stdout = self.main_proc.stdout.readline()
            main_proc_stdout = main_proc_stdout.decode("utf-8")
            print(main_proc_stdout.rstrip())
            if self.extra_folder_name == "" and self.main_proc_mgr.result_parent_dir in main_proc_stdout:
                start_idx = main_proc_stdout.find(self.main_proc_mgr.result_parent_dir)
                self.output_file_path = main_proc_stdout[start_idx:]

                result_dir = check_and_fix_dir_path(os.path.join(self.main_proc_mgr.result_parent_dir, self.dut))
                result_dir_str_len = len(result_dir)
                suffix = self.output_file_path[result_dir_str_len:]

                slash_idx = suffix.find('/')

                self.extra_folder_name = suffix[:slash_idx]

    def on_exiting(self):
        # Abort any running tests before exiting the gui.
        self.event_handler.save_gui_state()
        self.event_handler.abort_button_click()
        self.window.destroy()

    def check_magic(self, command):
        if command[0:7].upper() == "--MAGIC":
            path_settings_path = os.path.join(self.main_proc_mgr.gui_program_dir, "Path_Settings")
            path_settings = read_json_file_to_dict(path_settings_path + ".json")
            if command[8:].upper() == "ON":
                path_settings["magic"] = "on"
                self.title_label.set_label_color((0, 0, 0), (255, 0, 0))
                write_dict_to_json_file(path_settings, path_settings_path)

            elif command[8:].upper() == "OFF":
                path_settings["magic"] = "off"
                self.title_label.set_label_color((0, 0, 0), (0, 255, 0))
                write_dict_to_json_file(path_settings, path_settings_path)

            else:
                print("Unknown command.")

            self.DUT_entry.set_entry_text("")

            return True

        return False
