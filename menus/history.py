from . import MenuBase
from utils.persistent import History
from .statistics import StatisticsMenu
import tkinter.ttk as ttk
import tkinter as tk
import time


class HistoryMenu(MenuBase):
    def __init__(self, hist:History, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 560
        self.height = 300
        self.title = "Histórico"
        super().__init__(master, True)
        self.hist = hist

        stats = ttk.Button(self.mframe, default="active", text='Estatísticas', width=15, command=self.__open_statistics)
        stats.pack(anchor="w", padx=5, pady=10, side="top")

        frame2 = ttk.Frame(self.mframe, height=200, width=200)
        cols = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7']
        self.history_table = ttk.Treeview(frame2, selectmode="extended", show="headings", columns=cols, displaycolumns=cols)
        self.history_table.column("col1", anchor="w", stretch=True, width=70, minwidth=20)
        self.history_table.column("col2", anchor="w", stretch=True, width=115, minwidth=20)
        self.history_table.column("col3", anchor="center", stretch=True, width=60, minwidth=20)
        self.history_table.column("col4", anchor="w", stretch=True, width=85, minwidth=20)
        self.history_table.column("col5", anchor="center", stretch=True, width=75, minwidth=20)
        self.history_table.column("col6", anchor="center", stretch=True, width=75, minwidth=20)
        self.history_table.column("col7", anchor="center", stretch=True, width=50, minwidth=20)
        self.history_table.heading("col1", anchor="w", text='Pontuação')
        self.history_table.heading("col2", anchor="w", text='Dia e Horário')
        self.history_table.heading("col3", anchor="center", text='Duração')
        self.history_table.heading("col4", anchor="w", text='Dificuldade')
        self.history_table.heading("col5", anchor="center", text='Nº de minas')
        self.history_table.heading("col6", anchor="center", text='Minas marcadas')
        self.history_table.heading("col7", anchor="center", text='Vitória?')
        self.history_table.pack(expand=True, fill="both", side="left")
        
        scroll_x = ttk.Scrollbar(self.mframe, orient="horizontal", command=self.history_table.xview)
        scroll_y = ttk.Scrollbar(frame2, orient="vertical", command=self.history_table.yview)
        self.history_table.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        frame2.pack(expand=True, fill="both", padx=5, side="top")
        scroll_x.pack(expand=False, fill="x", padx=5, side="top")
        scroll_y.pack(expand=False, fill="y", side="left")
        self.mframe.pack(expand=True, fill="both", side="top")

        for items in hist:
            items[1] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(items[1]))
            items[3] = ("Fácil", "Médio", "Difícil", "Personalizado")[items[3]]
            items[6] = "Sim" if items[6] else "Não"
            self.history_table.insert('', 'end', values=items)
    
    def __open_statistics(self):
        top = tk.Toplevel(self.mainwindow)
        st = StatisticsMenu(self.hist, top)
        st.run()
