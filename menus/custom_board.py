import tkinter as tk
import tkinter.ttk as ttk
from menus import MenuBase


class CustomBoard(MenuBase):
    def __init__(self, master:tk.Tk|tk.Toplevel|None=None, diff_id:int=0):
        self.width = 300
        self.height = 190
        self.title = "Novo tabuleiro"
        super().__init__(master)

        ttk.Label(self.mframe, text='Nome:').place(anchor="nw", x=20, y=20)
        ttk.Label(self.mframe, text='Lado do tabuleiro:').place(anchor="nw", x=20, y=60)
        ttk.Label(self.mframe, text='Quantidade de minas:').place(anchor="nw", x=20, y=100)

        self.dific_name = ttk.Entry(self.mframe, width=30)
        self.side = ttk.Spinbox(self.mframe, justify="center", width=5)
        self.nmine = ttk.Spinbox(self.mframe, justify="center", width=5)

        self.delete = ttk.Button(self.mframe, text='Cancelar', width=13, command=self.mainwindow.destroy)
        self.delete.place(anchor="nw", x=188, y=150)
        self.confirm = ttk.Button(self.mframe, default="active", text='Salvar', width=13)
        self.confirm.place(anchor="nw", x=83, y=150)

        self.dific_name.place(anchor="nw", x=90, y=20)
        self.side.place(anchor="nw", x=226, y=60)
        self.nmine.place(anchor="nw", x=226, y=100)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomBoard(root)
    app.run()


