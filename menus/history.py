import tkinter as tk
import tkinter.ttk as ttk
from menus import MenuBase


class History(MenuBase):
    def __init__(self, master:tk.Tk|tk.Toplevel|None=None):
        self.width = 560
        self.height = 300
        self.title = "Histórico"
        super().__init__(master)
        self.mainwindow.resizable(1, 1)

        stats = ttk.Button(self.mframe, default="active", text='Estatísticas', width=15)
        stats.pack(anchor="w", padx=5, pady=10, side="top")

        frame2 = ttk.Frame(self.mframe, height=200, width=200)
        cols = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']
        self.history_table = ttk.Treeview(frame2, selectmode="extended", show="headings", columns=cols, displaycolumns=cols)
        self.history_table.column("col1", anchor="w", stretch=True, width=100, minwidth=20)
        self.history_table.column("col2", anchor="w", stretch=True, width=125, minwidth=20)
        self.history_table.column("col3", anchor="w", stretch=True, width=75, minwidth=20)
        self.history_table.column("col4", anchor="w", stretch=True, width=75, minwidth=20)
        self.history_table.column("col5", anchor="w", stretch=True, width=75, minwidth=20)
        self.history_table.column("col6", anchor="w", stretch=True, width=75, minwidth=20)
        self.history_table.heading("col1", anchor="w", text='Pontuação')
        self.history_table.heading("col2", anchor="w", text='Dia e Horário')
        self.history_table.heading("col3", anchor="w", text='Tabuleiro')
        self.history_table.heading("col4", anchor="w", text='Nº de minas')
        self.history_table.heading("col5", anchor="w", text='Minas marcadas')
        self.history_table.heading("col6", anchor="w", text='Vitória?')
        self.history_table.pack(expand=True, fill="both", side="left")
        
        scroll_x = ttk.Scrollbar(self.mframe, orient="horizontal", command=self.history_table.xview)
        scroll_y = ttk.Scrollbar(frame2, orient="vertical", command=self.history_table.yview)
        self.history_table.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        frame2.pack(expand=True, fill="both", padx=5, side="top")
        scroll_x.pack(expand=False, fill="x", padx=5, side="top")
        scroll_y.pack(expand=False, fill="y", side="left")
        self.mframe.pack(expand=True, fill="both", side="top")


if __name__ == "__main__":
    root = tk.Tk()
    app = History(root)
    app.run()


