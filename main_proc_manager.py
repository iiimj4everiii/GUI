from helpers import *
import subprocess


class MainProcMgr:

    main_proc = None

    def __init__(self, gui_program_dir):

        # MAIN_SCRIPT_PATH = "C:\\Users\\minjiang\\Documents\\Python\\gui\\main.py"

        self.gui_program_dir = check_and_fix_dir_path(gui_program_dir)

        path_settings = read_json_file_to_dict(os.path.join(self.gui_program_dir, "Path_Settings.json"))

        self.main_script_path = path_settings["main_script_path"]

        self.test_plan_file_dir = check_and_fix_dir_path(path_settings["test_plan_file dir"])

        self.bench_file_dir = check_and_fix_dir_path(path_settings["bench_file_dir"])

        self.result_parent_dir = check_and_fix_dir_path(path_settings["result_parent_dir"])

    def spawn(self, dut_name, test_plan_filename, bench_filename):

        python_version = get_python_version()
        test_plan_path = self.test_plan_file_dir + test_plan_filename
        bench_file_path = self.bench_file_dir + bench_filename

        if dut_name == "":
            dut_name = "DUMMY_DUT"

        makedir(self.result_parent_dir, dut_name)

        output_dir = os.path.join(self.result_parent_dir, dut_name)

        return subprocess.Popen([python_version, self.main_script_path, "-b", bench_file_path, "-p", "-i",
                                 test_plan_path, "--outputdir", output_dir, "-u", "false"], stdout=subprocess.PIPE)