from regras import *
from interface import Interface
import tkinter as tk

def reiniciar():
    engine = SistemaEspecialista()
    engine.gui = gui
    engine.reset()
    engine.declare(Luz(tipo=gui.escolha))
    engine.run()
    gui.escolha = None

if __name__ == "__main__":
    root = tk.Tk()
    
    gui = Interface(root)
    root.bind("<<EscolhaConcluida>>", lambda e: reiniciar())

    root.mainloop()
