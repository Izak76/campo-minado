from utils.persistent import History
from . import MenuBase
import tkinter.ttk as ttk
import tkinter as tk


class StatisticsMenu(MenuBase):
    def __init__(self, hist:History, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 400
        self.height = 200
        self.title = "Estatísticas"
        super().__init__(master)

        self.list_diffs = tk.Listbox(self.mframe, borderwidth=2, height=7, relief="groove", width=25, highlightthickness=0, selectmode="single", activestyle="none")
        self.list_diffs.insert('end', "Geral", "Fácil", "Médio", "Difícil", "Personalizado")
        self.list_diffs.bind("<<ListboxSelect>>", self.set_statistic)
        self.list_diffs.select_set(0)

        ok = ttk.Button(self.mframe, default="active", text='OK', width=14, command=self.mainwindow.destroy)
        frame1 = ttk.Frame(self.mframe, height=125, width=200)
        frame1.grid_propagate(False)

        ttk.Label(frame1, text='Partidas jogadas:').grid(column=0, pady=3, row=0, sticky="w")
        ttk.Label(frame1, text='Vitórias:').grid(column=0, pady=3, row=1, sticky="w")
        ttk.Label(frame1, text='Percentual de vitórias:').grid(column=0, ipadx=10, pady=3, row=2, sticky="w")
        ttk.Label(frame1, text='Maior pontuação:').grid(column=0, pady=3, row=3, sticky="w")
        ttk.Label(frame1, text='Menor tempo:').grid(column=0, pady=3, row=4, sticky="w")

        self.pj = ttk.Label(frame1)
        self.vit = ttk.Label(frame1)
        self.pv = ttk.Label(frame1)
        self.mp = ttk.Label(frame1)
        self.mt = ttk.Label(frame1)

        self.pj.grid(column=1, row=0, sticky="w")
        self.vit.grid(column=1, row=1, sticky="w")
        self.pv.grid(column=1, row=2, sticky="w")
        self.mp.grid(column=1, row=3, sticky="w")
        self.mt.grid(column=1, row=4, sticky="w")
        
        self.list_diffs.pack(anchor="n", padx=15, pady=15, side="left")
        frame1.pack(pady=12, side="top")
        ok.pack(anchor="e", padx=20, pady=10, side="top")

        # stats[dificuldade][part. jog.|vits.|maior p.|menor t.]
        self.__stats = tuple(([0]*4 for _ in range(4)))
        for h in hist:
            points, time, diff, vit = h[0], h[2], h[3], h[6]
            d = self.__stats[diff]

            d[0] += 1
            d[1] += vit

            if points > d[2]:
                d[2] = points
            
            if time < d[3] or not d[3]:
                d[3] = time
        
        self.set_statistic()
    
    def set_statistic(self, evt:tk.Event|None=None):
        index ,= self.list_diffs.curselection()

        if not index:
            get_items = lambda i: (x[i] for x in self.__stats)

            self.pj['text'] = sum(get_items(0))
            self.vit['text'] = sum(get_items(1))
            self.mp['text'] = max(get_items(2))
            self.mt['text'] = min(get_items(3))
        
        else:
            for idx, label in enumerate(map(self.__getattribute__, 'pj vit mp mt'.split())):
                label['text'] = self.__stats[index-1][idx]
        
        self.pv['text'] = f"{self.vit['text']/self.pj['text']*100:.1f}%"
            
