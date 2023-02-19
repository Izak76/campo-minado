from . import MenuBase
import tkinter.ttk as ttk
import tkinter as tk


class GameOptionsMenu(MenuBase):
    def __init__(self, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 325
        self.height = 225
        self.title = "Opções de jogo"
        super().__init__(master)

        self.game_opt = tk.IntVar(value=0)
        self.game_opt.trace_add("write", self.diff_opts_tracer)

        ttk.Radiobutton(self.mframe, text='Continuar jogando', value=0, variable=self.game_opt)\
            .grid(column=0, padx=20, pady=5, row=0, sticky="w")
        ttk.Radiobutton(self.mframe, text='Iniciar um novo jogo', value=1, variable=self.game_opt)\
            .grid(column=0, padx=20, pady=5, row=1, sticky="w")
        ttk.Radiobutton(self.mframe, text='Iniciar novo jogo em uma dificuldade diferente', value=2, variable=self.game_opt)\
            .grid(column=0, padx=20, pady=5, row=2, sticky="w")
        ttk.Radiobutton(self.mframe, text='Reiniciar o jogo', value=3, variable=self.game_opt)\
            .grid(column=0, padx=20, pady=10, row=4, sticky="w")
        ttk.Button(self.mframe, default="active", text='OK', width=13)\
            .grid(column=0, pady=10, row=5, sticky="e")

        self.diff_opts = ttk.Combobox(self.mframe, state="disabled", width=30)
        self.diff_opts["values"] = ["Fácil (9x9, 10 minas)", "Médio (16x16, 40 minas)", "Difícil (25x25, 125 minas)", "Personalizado..."]
        self.diff_opts.grid(column=0, row=3)

        self.mframe.place(y=15)
    
    def diff_opts_tracer(self, *args):
        if self.game_opt.get() == 2:
            self.diff_opts["state"] = "readonly"
        
        else:
            self.diff_opts["state"] = "disabled"
