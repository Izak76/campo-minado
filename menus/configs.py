import tkinter as tk
import tkinter.ttk as ttk
import re
from menus import MenuBase


class Configs(MenuBase):
    def __init__(self, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 336
        self.height = 360
        self.title = "Configurações de jogo"
        super().__init__(master)

        self.color = tk.IntVar(self.mframe, 0)
        self.cwidth = tk.StringVar(self.mframe, name="width")
        self.cheight = tk.StringVar(self.mframe, name="height")
        self.res = tk.IntVar(self.mframe, 0)
        self.sound = tk.BooleanVar(self.mframe)
        self.save_on_exit = tk.BooleanVar(self.mframe)

        self.res.trace_add('write', self.res_trace)
        self.wh_trace(True)

        lf1 = ttk.Labelframe(self.mframe, height=80, text='Cor dos quadrados', width=285)
        lf2 = ttk.Labelframe(self.mframe, height=85, text='Resolução', width=285)

        self.ew = ttk.Entry(lf2, justify="center", state="disabled", textvariable=self.cwidth, width=5)
        self.eh = ttk.Entry(lf2, justify="center", state="disabled", textvariable=self.cheight, width=5)

        ttk.Button(self.mframe, default="active", text='OK', width=13).place(anchor="nw", x=115, y=315)
        ttk.Button(self.mframe, text='Cancelar', width=13, command=self.mainwindow.destroy).place(anchor="nw", x=220, y=315)
        ttk.Checkbutton(self.mframe, offvalue=0, onvalue=1, text='Reproduzir sons', variable=self.sound).place(anchor="nw", x=20, y=250)
        ttk.Checkbutton(self.mframe, offvalue=0, onvalue=1, text='Salvar jogo ao sair', variable=self.save_on_exit).place(anchor="nw", x=20, y=280)
        ttk.Combobox(self.mframe, state="readonly",
            values=["Fácil (9x9, 10 minas)", "Médio (16x16, 40 minas)", "Difícil (25x25, 125 minas)", "Personalizado..."],
            width=30).place(anchor="nw", x=100, y=21)
        ttk.Label(self.mframe, text='Dificuldade:').place(anchor="nw", x=20, y=20)
        ttk.Label(lf2, text='x').grid(column=2, row=1)
        ttk.Radiobutton(lf1, text='Azul', value=0, variable=self.color).grid(column=0, padx=10, pady=5, row=0, sticky="nw")
        ttk.Radiobutton(lf1, text='Verde', value=1, variable=self.color).grid(column=1, row=0, sticky="w")
        ttk.Radiobutton(lf1, text='Amarelo', value=2, variable=self.color).grid(column=2, padx=5, row=0, sticky="w")
        ttk.Radiobutton(lf1, text='Laranja', value=3, variable=self.color).grid(column=0, ipadx=5, padx=10, row=1, sticky="w")
        ttk.Radiobutton(lf1, text='Azul Claro', value=4, variable=self.color).grid(column=1, ipadx=5, row=1, sticky="w")
        ttk.Radiobutton(lf2, text='640 x 480', value=0, variable=self.res).grid(column=0, ipady=5, padx=5, row=0, sticky="w")
        ttk.Radiobutton(lf2, text='960 x 720', value=2, variable=self.res).grid(column=0, padx=5, row=1, sticky="w")
        ttk.Radiobutton(lf2, text='800 x 600', value=1, variable=self.res).grid(column=1, padx=5, row=0, sticky="w")
        ttk.Radiobutton(lf2, text='1024 x 768', value=3, variable=self.res).grid(column=1, ipadx=3, padx=5, row=1, sticky="w")
        ttk.Radiobutton(lf2, text='Personalizado', value=4, variable=self.res).grid(column=2, ipady=3, row=0, sticky="w")
        
        lf1.place(x=20, y=55)
        lf2.place(anchor="nw", x=20, y=150)
        self.ew.grid(column=2, row=1, sticky="w")
        self.eh.grid(column=2, row=1, sticky="e")  

        lf1.grid_propagate(False)
        lf2.grid_propagate(False)
    
    def res_trace(self, *args:tuple[str]):
        entries = (self.ew, self.eh)
        if self.res.get() == 4:
            for e in entries:
                e['state'] = "normal"
        
        else:
            for e in entries:
                e['state'] = "disabled"
    
    def custom_res_trace(self, name:str, *args:tuple[str]):
        self.wh_trace(False)
        var = self.cwidth if name == "width" else self.cheight
        try:
            v = int("".join(re.findall(r'\d', var.get())))
        except ValueError:
            self.cwidth.set('')
            self.cheight.set('')
            self.wh_trace(True)
            return

        var.set(str(v))

        if name == "width":
            self.cheight.set(3*v//4)

        elif name == "height":
            self.cwidth.set(4*v//3)
        
        self.wh_trace(True)

    def wh_trace(self, enable:bool):
        if enable:
            self.cwidth.trace_add('write', self.custom_res_trace)
            self.cheight.trace_add('write', self.custom_res_trace)

        else:
            self.cwidth.trace_remove("write", self.cwidth.trace_info()[0][1])
            self.cheight.trace_remove("write", self.cheight.trace_info()[0][1])

if __name__ == "__main__":
    root = tk.Tk()
    app = Configs(root)
    app.run()


