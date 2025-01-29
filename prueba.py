import tkinter as tk
from tkinter import ttk
import threading
import time


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter con Threading")

        self.start_button = ttk.Button(root, text="Iniciar", command=self.start_task)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(
            root, text="Detener", command=self.stop_task, state=tk.DISABLED
        )
        self.stop_button.pack(pady=10)

        self.status_label = ttk.Label(root, text="Estado: Inactivo")
        self.status_label.pack(pady=10)

        self.running = False

    def start_task(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Estado: Ejecutando")

            # Iniciar la tarea en un hilo separado
            self.thread = threading.Thread(target=self.long_running_task)
            self.thread.start()

    def stop_task(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Estado: Deteniendo...")

    def long_running_task(self):
        for i in range(1, 101):
            if not self.running:
                break

            # Simular una tarea que toma tiempo
            time.sleep(0.1)

            # Actualizar la interfaz gráfica (esto debe hacerse en el hilo principal)
            self.root.after(0, self.update_status, i)

        # Finalizar la tarea
        self.root.after(0, self.task_completed)

    def update_status(self, progress):
        self.status_label.config(text=f"Estado: Progreso {progress}%")

    def task_completed(self):
        self.status_label.config(text="Estado: Inactivo")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
