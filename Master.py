import tkinter as tk
import random
from tkinter import messagebox, Toplevel
import pygame
from itertools import permutations

# Inicializar la música de fondo con pygame
pygame.mixer.init()

# Colores posibles (7 colores)
COLORES = ['Rojo', 'Azul', 'Verde', 'Amarillo', 'Morado', 'Naranja', 'Rosado']

# Diccionario para mapear colores en español con sus valores de color
MAPA_COLORES = {
    'Rojo': 'red',
    'Azul': 'blue',
    'Verde': 'green',
    'Amarillo': 'yellow',
    'Morado': 'purple',
    'Naranja': 'orange',
    'Rosado': 'pink'
}

# Generar combinación secreta aleatoria de 5 colores
def generar_combinacion():
    return random.sample(COLORES, 5)

# Comparar intento con la combinación secreta y devolver las pistas

def evaluar_intento(combinacion_secreta, intento):
    # Paso 1: Contar colores correctos en la posición correcta
    correctos_y_posicion = sum([1 for i in range(5) if intento[i] == combinacion_secreta[i]])

    # Paso 2: Contar colores correctos sin importar la posición
    # Crear copias de las listas para no modificar las originales
    combinacion_secreta_temp = combinacion_secreta.copy()
    intento_temp = intento.copy()

    # Eliminar los colores que ya han sido contados como correctos y en posición correcta
    for i in range(5):
        if intento[i] == combinacion_secreta[i]:
            combinacion_secreta_temp[i] = None  # Marcar como usado
            intento_temp[i] = None  # Marcar como usado

    # Contar cuántos colores del intento están en la combinación secreta pero en posiciones incorrectas
    correctos_sin_posicion = 0
    for color in intento_temp:
        if color and color in combinacion_secreta_temp:
            correctos_sin_posicion += 1
            # Marcar el color como usado para evitar duplicados
            combinacion_secreta_temp[combinacion_secreta_temp.index(color)] = None

    # El total de colores adivinados debe incluir los que están en la posición correcta
    total_colores_adivinados = correctos_y_posicion + correctos_sin_posicion

    return correctos_y_posicion, total_colores_adivinados
# Clase principal del juego
class Mastermind(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mastermind - Adivina la combinación de colores")
        self.geometry("900x700")
        self.config(bg="lightgray")
        
        pygame.mixer.music.load("musica_fondo.mp3")
        pygame.mixer.music.play(-1)

        self.combinacion_secreta = generar_combinacion()
        self.intentos = []
        self.max_intentos = 5

        # Para almacenar colores y posiciones adivinadas
        self.colores_adivinados = set()
        self.posiciones_adivinadas = set()

        self.label_titulo = tk.Label(self, text="MASTERMIND", font=("Arial", 24, "bold"), bg="lightgray", fg="black")
        self.label_titulo.pack(pady=10)

        self.label_colores = tk.Label(self, text="Listado de colores disponibles:", font=("Arial", 14), bg="lightgray", fg="black")
        self.label_colores.pack(pady=5)
        
        self.canvas = tk.Canvas(self, width=550, height=400, bg='white', highlightbackground="black")
        self.canvas.pack(pady=10)

        self.botones_colores = []
        for i, color in enumerate(COLORES):
            btn = tk.Button(self, text=color, bg=MAPA_COLORES[color], width=8, command=lambda c=color: self.seleccionar_color(c))
            btn.place(x=130 + i * 70, y=550)
            self.botones_colores.append(btn)
        
        self.label_intento = tk.Label(self, text="Selecciona 5 colores:", font=("Arial", 10), bg="lightgray", fg="black")
        self.label_intento.pack(pady=(0,35))

        self.btn_validar = tk.Button(self, text="Validar intento", font=("Arial", 12, "bold"), command=self.validar_intento)
        self.btn_validar.pack(pady=0)
        
        self.btn_reiniciar = tk.Button(self, text="Reiniciar juego", font=("Arial", 12, "bold"), command=self.reiniciar_juego)
        self.btn_reiniciar.pack(pady=5)

        self.btn_sugerir = tk.Button(self, text="Sugerir posible solución", font=("Arial", 12, "bold"), command=self.sugerir_solucion)
        self.btn_sugerir.pack(pady=5)

        self.intento_actual = []

        # Etiquetas adicionales para mostrar colores y posiciones adivinadas
        self.label_colores_adivinados = tk.Label(self, text="Colores adivinados: ", font=("Arial", 10,"bold"), bg="lightgray", fg="black")
        self.label_colores_adivinados.place(x=730, y=105)
        self.label_posiciones_adivinadas = tk.Label(self, text="En posición correcta: ", font=("Arial", 10,"bold"), bg="lightgray", fg="black")
        self.label_posiciones_adivinadas.place(x=730, y=350)

    def seleccionar_color(self, color):
        if len(self.intento_actual) < 5 and color not in self.intento_actual:
            self.intento_actual.append(color)
            self.dibujar_intento()

    def dibujar_intento(self):
        self.canvas.delete("intento")
        for i, color in enumerate(self.intento_actual):
            self.canvas.create_oval(20 + i * 60, 270, 70 + i * 60, 320, fill=MAPA_COLORES[color], tags="intento")

    def validar_intento(self):
        if len(self.intento_actual) == 5:
            correctos_y_posicion, correctos_sin_posicion = evaluar_intento(self.combinacion_secreta, self.intento_actual)
            self.intentos.append((self.intento_actual, correctos_y_posicion, correctos_sin_posicion))
            self.mostrar_intentos()

            # Guardar los colores y posiciones adivinadas
            for i, color in enumerate(self.intento_actual):
                if color in self.combinacion_secreta and color not in self.colores_adivinados:
                    self.colores_adivinados.add(color)
                if color == self.combinacion_secreta[i] and i not in self.posiciones_adivinadas:
                    self.posiciones_adivinadas.add(i)

            self.actualizar_colores_y_posiciones_adivinadas()

            self.intento_actual = []
            self.canvas.delete("intento")

            if correctos_y_posicion == 5:
                self.mostrar_ganador()
            elif len(self.intentos) >= self.max_intentos:
                self.mostrar_perdedor()

    def mostrar_intentos(self):
        self.canvas.delete("intentos_previos")
        for idx, (intento, correctos_y_posicion, correctos_sin_posicion) in enumerate(self.intentos):
            for i, color in enumerate(intento):
                self.canvas.create_oval(20 + i * 60, 20 + idx * 60, 70 + i * 60, 70 + idx * 60, fill=MAPA_COLORES[color], tags="intentos_previos")
            self.canvas.create_text(410, 40 + idx * 60, text=f"Adivinados: {correctos_sin_posicion}, Posición correcta: {correctos_y_posicion}", font=("Arial", 9, "bold"), tags="intentos_previos")

    def actualizar_colores_y_posiciones_adivinadas(self):
        # Borrar cualquier etiqueta existente antes de actualizar
        for widget in self.label_colores_adivinados.winfo_children():
            widget.destroy()
        for widget in self.label_posiciones_adivinadas.winfo_children():
            widget.destroy()

        # Actualizar colores adivinados en formato vertical
        label_colores_titulo = tk.Label(self.label_colores_adivinados, text="Colores adivinados: ", font=("Arial", 10,"bold"), bg="lightgray", fg="black")
        label_colores_titulo.pack()

        for color in self.colores_adivinados:
            label = tk.Label(self.label_colores_adivinados, text=color, font=("Arial", 10), bg="lightgray", fg="black")
            label.pack()

        # Actualizar colores en posición correcta en formato vertical
        label_posiciones_titulo = tk.Label(self.label_posiciones_adivinadas, text="En posición correcta: ", font=("Arial", 10,"bold"), bg="lightgray", fg="black")
        label_posiciones_titulo.pack()

        posiciones = [self.combinacion_secreta[i] for i in self.posiciones_adivinadas]
        for color in posiciones:
            label = tk.Label(self.label_posiciones_adivinadas, text=color, font=("Arial", 10), bg="lightgray", fg="black")
            label.pack()

    def mostrar_ganador(self):
        messagebox.showinfo("¡Ganaste!", "¡Felicitaciones, has adivinado la combinación!")
        self.reiniciar_juego()

    def mostrar_perdedor(self):
        respuesta = messagebox.askyesno("Perdiste", f"La combinación secreta era {self.combinacion_secreta}. ¿Quieres volver a jugar?")
        if respuesta:
            self.reiniciar_juego()
        else:
            self.quit()

    def reiniciar_juego(self):
        self.combinacion_secreta = generar_combinacion()
        self.intentos = []
        self.intento_actual = []
        self.colores_adivinados.clear()
        self.posiciones_adivinadas.clear()
        self.label_colores_adivinados.config(text="Colores adivinados: ")
        self.label_posiciones_adivinadas.config(text="En posición correcta: ")
        self.canvas.delete("intentos_previos")
        self.canvas.delete("intento")

    def sugerir_solucion(self):
        ventana_sugerencias = Toplevel(self)
        ventana_sugerencias.title("Sugerencias de posibles soluciones")
        ventana_sugerencias.geometry("440x420")

        label_info = tk.Label(ventana_sugerencias, text="Posibles combinaciones basadas en los intentos previos:", font=("Arial", 12,"bold"))
        label_info.pack(pady=10)

        combinaciones_posibles = self.generar_posibles_combinaciones()

        for idx, combinacion in enumerate(combinaciones_posibles):
            label = tk.Label(ventana_sugerencias, text=f"{idx + 1}. {combinacion}")
            label.pack(pady=5)

    def generar_posibles_combinaciones(self):
        combinaciones_validas = []
        for permutacion in permutations(COLORES, 5):
            es_valida = True
            for intento, correctos_y_posicion, correctos_sin_posicion in self.intentos:
                pista_intento = evaluar_intento(list(permutacion), intento)
                if pista_intento != (correctos_y_posicion, correctos_sin_posicion):
                    es_valida = False
                    break
            if es_valida:
                combinaciones_validas.append(permutacion)
        
        combinaciones_filtradas = [p for p in combinaciones_validas if all(p[i] == self.combinacion_secreta[i] for i in self.posiciones_adivinadas)]
        
        return combinaciones_filtradas[:10] if combinaciones_filtradas else combinaciones_validas[:10]

# Ejecutar el juego
if __name__ == "__main__":
    juego = Mastermind()
    juego.mainloop()
