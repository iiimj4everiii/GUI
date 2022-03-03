from helpers import *
import subprocess


class MainProcMgr:

    main_proc = None

    def __init__(self, gui_program_dir):

        # MAIN_SCRIPT_PATH = "C:\\Users\\minjiang\\Documents\\Python\\gui\\main.py"

        self.python_version = "python"   # get_python_version()

        self.gui_program_dir = check_and_fix_dir_path(gui_program_dir)

        # Parse Path_Settings.json file
        path_settings = read_json_file_to_dict(os.path.join(self.gui_program_dir, "Path_Settings.json"))

        self.main_script_path = path_settings["main_script_path"]
        self.test_plan_file_dir = check_and_fix_dir_path(path_settings["test_plan_file dir"])
        self.bench_file_dir = check_and_fix_dir_path(path_settings["bench_file_dir"])
        self.result_parent_dir = check_and_fix_dir_path(path_settings["result_parent_dir"])

        # Getting Telecaster Version
        proc = subprocess.Popen([self.python_version, self.main_script_path, "--version"], stdout=subprocess.PIPE)

        # Wait until proc is done.
        while proc.poll() is None:
            pass

        proc_stdout = get_line_from_proc_stdout(proc)
        while "RFDate Revision:" not in proc_stdout:
            proc_stdout = get_line_from_proc_stdout(proc)

        start_idx = proc_stdout.find("RFDate Revision:")
        self.tc_version_str = proc_stdout[start_idx:]

    def spawn(self, dut_name, test_plan_filename, bench_filename):

        test_plan_path = self.test_plan_file_dir + test_plan_filename
        bench_file_path = self.bench_file_dir + bench_filename

        if dut_name == "":
            dut_name = "DUMMY_DUT"

        makedir(self.result_parent_dir, dut_name)

        output_dir = os.path.join(self.result_parent_dir, dut_name)

        return subprocess.Popen([self.python_version, self.main_script_path, "-b", bench_file_path, "-p", "-i",
                                 test_plan_path, "--outputdir", output_dir, "-u", "false"], stdout=subprocess.PIPE)
