# ------------------------------------------ #
#              Libras Detector               #
# ------------------------------------------ #
#               Programadores:               #
#         Fernando Martins Ferreira          #
#           Kaua Alves Nascimento            #
#             Steffany Medeiros              #
# ------------------------------------------ #
#        Samsung Innovation Campus           #
# ------------------------------------------ #

import tkinter as tk
from tela_video import create_screen

root = tk.Tk()
root.title("Samsung Innovation Campus - Libras Detector")
root.geometry("800x650")

frame1 = create_screen(root)

frame1.place(relwidth=1, relheight=1)

frame1.tkraise()

root.mainloop()
