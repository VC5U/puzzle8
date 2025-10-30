import streamlit as st
from collections import deque
import time

# =====================
# Configuración inicial
# =====================
st.set_page_config(page_title="Puzzle 8 - Agente Inteligente", layout="centered")
st.title("Puzzle 8 - Resolución con Agente BFS")
st.write("Este ejemplo muestra cómo un agente inteligente resuelve el Puzzle 8 usando Búsqueda en Anchura (BFS).")

# Estado inicial y objetivo
estado_inicial = [1, 2, 3, 4, 0, 5, 6, 7, 8]  # Puedes cambiar este estado
estado_objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# =====================
# Funciones auxiliares
# =====================
def mover(estado):
    movimientos = []
    index = estado.index(0)
    fila, col = index // 3, index % 3
    direcciones = {'Arriba': (-1,0), 'Abajo': (1,0), 'Izquierda': (0,-1), 'Derecha': (0,1)}
    for d, (dr, dc) in direcciones.items():
        nueva_fila, nueva_col = fila + dr, col + dc
        if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
            nuevo_index = nueva_fila*3 + nueva_col
            nuevo_estado = estado.copy()
            nuevo_estado[index], nuevo_estado[nuevo_index] = nuevo_estado[nuevo_index], nuevo_estado[index]
            movimientos.append((d, nuevo_estado))
    return movimientos

def bfs(inicial, objetivo):
    cola = deque([(inicial, [])])
    visitados = set()
    while cola:
        estado_actual, path = cola.popleft()
        if estado_actual == objetivo:
            return path
        visitados.add(tuple(estado_actual))
        for movimiento, nuevo_estado in mover(estado_actual):
            if tuple(nuevo_estado) not in visitados:
                cola.append((nuevo_estado, path + [nuevo_estado]))
    return None

def mostrar_tablero(tablero):
    tablero_3x3 = [tablero[i:i+3] for i in range(0, 9, 3)]
    st.table(tablero_3x3)

# =====================
# Interfaz interactiva
# =====================
st.subheader("Estado inicial")
mostrar_tablero(estado_inicial)

if st.button("Resolver Puzzle 8"):
    st.subheader("Resolviendo...")
    solucion = bfs(estado_inicial, estado_objetivo)
    if solucion:
        st.success(f"¡Solución encontrada en {len(solucion)} pasos!")
        st.subheader("Secuencia de movimientos:")
        for paso, estado in enumerate(solucion, start=1):
            st.write(f"Paso {paso}:")
            mostrar_tablero(estado)
            time.sleep(0.5)  # Pausa para animación
    else:
        st.error("No se encontró solución")
