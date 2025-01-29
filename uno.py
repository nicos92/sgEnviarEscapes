import threading
import pyautogui
import re
from colores import *
import time
from tkinter import *

# adv import io


class App:
    def __init__(self, root):
        # adv self.archivo = open("archivo")
        self.root: Tk = root
        self.root.config(bg=MisColores.White)
        self.root.title("Enviar Escapes")
        # self.root.bind("<Return>", lambda event: self.BtnDetener.invoke())

        # * variables
        self.esc = StringVar()
        self.esc.set("3")

        self.seg = StringVar()
        self.seg.set("5")

        self.vcmd = self.root.register(self.callback)

        self.running = False

        self.estado = StringVar()
        self.estado.set("Estado: Inactivo")

        # * WIDGET
        self.topFrame = Frame(
            master=root,
            width=200,
            height=300,
            padx=8,
            pady=8,
            bg=MisColores.White,
        )
        self.topFrame.pack()

        self.LblEstado = Label(
            master=self.topFrame,
            textvariable=self.estado,
            bg=MisColores.White,
            foreground=MisColores.Black,
            font=("Candara", 14, "normal"),
        )
        self.LblEstado.pack()

        self.mainFrame = Frame(
            master=root, width=200, height=300, padx=8, pady=8, bg=MisColores.White
        )
        self.mainFrame.pack()

        self.lblCantEsc = Label(
            master=self.mainFrame,
            text="Cantidad de ESC: ",
            padx=8,
            pady=8,
            bg=MisColores.White,
            foreground=MisColores.Black,
        )
        self.lblCantEsc.grid(row=0, column=0)

        self.txtCantEsc = Entry(
            master=self.mainFrame,
            textvariable=self.esc,
            validate="key",
            bg=MisColores.Light,
            foreground=MisColores.Black,
            validatecommand=(self.vcmd, "%P"),
        )
        self.txtCantEsc.grid(row=0, column=1)
        self.txtCantEsc.bind("<Return>", lambda event: self.BtnIniciar.invoke())

        self.interSeg = Label(
            master=self.mainFrame,
            text="Intervalo en Segundos: ",
            padx=8,
            pady=8,
            bg=MisColores.White,
            foreground=MisColores.Black,
        )
        self.interSeg.grid(row=1, column=0)

        self.txtCantSeg = Entry(
            master=self.mainFrame,
            textvariable=self.seg,
            validate="key",
            bg=MisColores.Light,
            foreground=MisColores.Black,
            validatecommand=(self.vcmd, "%P"),
        )
        self.txtCantSeg.grid(row=1, column=1)
        self.txtCantSeg.bind("<Return>", lambda event: self.BtnIniciar.invoke())

        # * BOTONES
        self.BtnIniciar = Button(
            master=self.mainFrame,
            text="Iniciar",
            bg=MisColores.Success,
            foreground=MisColores.Light,
            cursor="hand2",
            command=lambda: self.arrancando(),
        )
        self.BtnIniciar.grid(row=2, column=0, sticky="wens", padx=8, pady=6)

        self.BtnDetener = Button(
            master=self.mainFrame,
            text="Detener",
            bg=MisColores.Danger,
            foreground=MisColores.Light,
            cursor="arrow",
            command=lambda: self.detener(),
            state="disabled",
        )
        self.BtnDetener.grid(row=2, column=1, sticky="wens", padx=8, pady=6)
        self.BtnDetener.bind("<Return>", lambda event: self.BtnDetener.invoke())

        self.txtCantEsc.focus()

    # * FUNCIONES
    def callback(self, P):
        # Expresión regular que permite letras, números y espacios
        pattern = r"^[0-9]{0,2}$"
        # Verifica si el nuevo texto coincide con el patrón
        return bool(re.match(pattern, P))

    def arrancando(self):
        if not self.running:
            self.running = True
            self.txtCantEsc.config(state="disabled")
            self.txtCantSeg.config(state="disabled")
            self.BtnIniciar.config(state="disabled", cursor="arrow")
            self.BtnDetener.config(state="normal", cursor="hand2")
            self.BtnDetener.focus()

            self.thread = threading.Thread(target=self.arrancarEscapes)
            self.thread.start()

    def arrancarEscapes(self):
        self.estado.set("Estado: Activo")
        for i in range(int(self.esc.get())):
            contador = 1
            contador += i

            time.sleep(int(self.seg.get()))
            if not self.running:
                break
            self.root.after(0, self.progreso, contador)
            pyautogui.press("esc")

        # Finalizar la tarea
        self.root.after(0, self.Detenido)

    def progreso(self, i):
        self.estado.set(f"Estado: Escape Nº{i}")

    def detener(self):
        if self.running:
            self.Detenido()

    def Detenido(self):
        self.running = False
        self.txtCantEsc.config(state="normal")
        self.txtCantSeg.config(state="normal")
        self.BtnIniciar.config(state="normal", cursor="hand2")
        self.BtnDetener.config(state="disabled", cursor="arrow")
        self.estado.set("Estado: Inactivo")
        self.txtCantEsc.focus()


if __name__ == "__main__":
    root = Tk()

    root.resizable(False, False)

    root.iconbitmap(r"F:\Sistemas NoTocar\NICOS\sg\ESC1.ico")
    app = App(root=root)
    root.mainloop()
