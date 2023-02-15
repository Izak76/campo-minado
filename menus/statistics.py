import tkinter as tk
import tkinter.ttk as ttk
from menus import MenuBase


class Statistics(MenuBase):
    def __init__(self, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 400
        self.height = 180
        self.title = "Estatísticas"
        super().__init__(master)

        self.list_diffs = tk.Listbox(self.mframe, borderwidth=2, height=6, relief="groove", width=25, highlightthickness=0, activestyle="none")
        for d in ("Geral", "Fácil", "Médio", "Difícil", "Personalizado"):
            self.list_diffs.insert('end', d)
        self.list_diffs.select_set(0)

        ok = ttk.Button(self.mframe, default="active", text='OK', width=14, command=self.mainwindow.destroy)
        frame1 = ttk.Frame(self.mframe, height=100, width=200)
        frame1.grid_propagate(False)

        ttk.Label(frame1, text='Partidas jogadas:').grid(column=0, pady=3, row=0, sticky="w")
        ttk.Label(frame1, text='Vitórias:').grid(column=0, pady=3, row=1, sticky="w")
        ttk.Label(frame1, text='Derrotas:').grid(column=0, pady=3, row=2, sticky="w")
        ttk.Label(frame1, text='Percentual de vitórias:').grid(column=0, ipadx=10, pady=3, row=3, sticky="w")

        self.pj = ttk.Label(frame1)
        self.vit = ttk.Label(frame1)
        self.der = ttk.Label(frame1)
        self.pv = ttk.Label(frame1)

        self.pj.grid(column=1, row=0, sticky="w")
        self.vit.grid(column=1, row=1, sticky="w")
        self.der.grid(column=1, row=2, sticky="w")
        self.pv.grid(column=1, row=3, sticky="w")
        
        self.list_diffs.pack(anchor="n", padx=15, pady=15, side="left")
        frame1.pack(pady=15, side="top")
        ok.pack(anchor="e", padx=20, pady=10, side="top")


if __name__ == "__main__":
    root = tk.Tk()
    app = Statistics(root)
    app.run()
