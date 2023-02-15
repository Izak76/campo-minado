from tkinter import Tk, Toplevel, ttk

class MenuBase:
    def __init__(self, master:Tk|Toplevel|None=None):
        self.mframe = ttk.Frame(master, height=self.height, width=self.width)
        self.mainwindow = master if master else self.mframe

        if master:
            master.title(self.title)
            master.resizable(0, 0)
            center_window(master, self.width, self.height)
        
        self.mframe.pack(side="top")
    
    def run(self):
        self.mainwindow.mainloop()
    
    def destroy(self):
        self.mframe.destroy()

def center_window(root:Tk|Toplevel, width:int, height:int):
    root.update_idletasks()
    frm_width = root.winfo_rootx() - root.winfo_x()
    root.obj_width = width + 2 * frm_width
    titlebar_height = root.winfo_rooty() - root.winfo_y()
    root.obj_height = height + titlebar_height + frm_width
    x = root.winfo_screenwidth() // 2 - root.obj_width // 2
    y = root.winfo_screenheight() // 2 - root.obj_height // 2
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.deiconify()