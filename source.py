from main_proc_manager import MainProcMgr
from tc_gui import TCGUI


# GUI_PROGRAM_DIR = "/Applications/RFDATE_GUI/"
GUI_PROGRAM_DIR = "C:\\Users\\minjiang\\Documents\\Python\\GUI"

main_proc_mgr = MainProcMgr(GUI_PROGRAM_DIR)

G = TCGUI(main_proc_mgr)

G.window.mainloop()
