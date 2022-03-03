from main_proc_manager import MainProcMgr
from gui import GUIProcess
from tc_gui_widget_event_handler import TCGUIWidgetEventHandler
from helpers import *


class TCGUI(GUIProcess):

    def __init__(self, main_proc_mgr: MainProcMgr):
        super().__init__()

        self.dut = ""

        self.output_file_path = ""

        self.extra_folder_name_prefix = "Tests"
        self.extra_folder_name = ""
        self.new_extra_folder_name = ""
        self.comment = ""

        WINDOW_WIDTH = 900
        WINDOW_HEIGHT = 700

        self.setup_window("Telecaster", WINDOW_WIDTH, WINDOW_HEIGHT)

        self.title_label = self.create_label(0, 35)
        self.title_label.set_label_text("Telecaster GUI", text_size=32, text_weight="bold")
        self.title_label.set_label_color((0, 0, 0), (0, 255, 0))
        self.title_label.center_pos_x()

        self.main_proc_mgr = main_proc_mgr

        self.main_proc = None

        self.tc_ver_label = self.create_label(0, 90)
        self.tc_ver_label.set_label_text(self.main_proc_mgr.tc_version_str, text_size=10, text_weight="bold")
        self.tc_ver_label.set_label_color((0, 0, 0), (0, 255, 0))
        self.tc_ver_label.center_pos_x()

        LEFT_LIMIT = 175
        ENTRY_WIDTH = 675

        DUT_label, self.DUT_entry = self.Telecaster_entry(0, 150, "DUT: ", LEFT_LIMIT, 150, ENTRY_WIDTH)
        DUT_label.right_justify(LEFT_LIMIT)

        comment_label, self.comment_entry = self.Telecaster_entry(0, 225, "Comment: ", LEFT_LIMIT, 225, ENTRY_WIDTH)
        comment_label.right_justify(LEFT_LIMIT)

        tp_label, self.tp_entry = self.Telecaster_entry(0, 300, "Test Plan: ", LEFT_LIMIT, 300, ENTRY_WIDTH)
        tp_label.right_justify(LEFT_LIMIT)

        bench_label, self.bench_entry = self.Telecaster_entry(0, 375, "Bench File: ", LEFT_LIMIT, 375, ENTRY_WIDTH)
        bench_label.right_justify(LEFT_LIMIT)

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

        return label, entry

    def main_proc_polling(self):
        while True:
            if self.main_proc is None:
                return

            if self.main_proc.poll() is not None:
                self.main_proc = None
                self.event_handler.reset_gui_state()

                result_dir = os.path.join(self.main_proc_mgr.result_parent_dir, self.dut)
                os.rename(src=os.path.join(result_dir, self.extra_folder_name),
                          dst=os.path.join(result_dir, self.new_extra_folder_name))

                self.extra_folder_name = ""
                self.new_extra_folder_name = ""

                return

            main_proc_stdout = get_line_from_proc_stdout(self.main_proc)
            print(main_proc_stdout.rstrip())
            if self.extra_folder_name == "" and self.main_proc_mgr.result_parent_dir in main_proc_stdout:
                start_idx = main_proc_stdout.find(self.main_proc_mgr.result_parent_dir)
                self.output_file_path = main_proc_stdout[start_idx:]

                result_dir = check_and_fix_dir_path(os.path.join(self.main_proc_mgr.result_parent_dir, self.dut))
                result_dir_str_len = len(result_dir)
                suffix = self.output_file_path[result_dir_str_len:]

                slash_idx = suffix.find('/')

                self.extra_folder_name = suffix[:slash_idx]

                if self.comment != "":
                    self.new_extra_folder_name = self.extra_folder_name.replace(self.extra_folder_name_prefix,
                                                                                self.comment)

    def on_exiting(self):
        # Abort any running tests before exiting the gui.
        self.event_handler.save_gui_state()
        self.event_handler.abort_button_click()
        self.window.destroy()

    def check_magic(self, command):
        if command[0:2].upper() == "--":

            self.DUT_entry.set_entry_text("")

            if command[2:7].upper() == "MAGIC":
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

                return True

        return False
