import streamlit as st
from collections import deque
import time

# =====================
# Configuración inicial
# =====================
st.set_page_config(page_title="Puzzle 8 Interactivo", layout="centered")
st.title("Puzzle 8 Interactivo")
st.write("Mueve las fichas para resolver el Puzzle 8 manualmente o presiona 'Resolver automáticamente' para ver la solución del agente BFS.")

# Estado inicial
if "tablero" not in st.session_state:
    st.session_state.tablero = [1, 2, 3, 4, 0, 5, 6, 7, 8]

estado_objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0]
emojis = ["⬜","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣"]
colores = ["#FFFFFF","#FF9999","#99FF99","#9999FF","#FFCC99","#99FFCC","#CC99FF","#FF99CC","#99CCFF"]

# =====================
# Funciones
# =====================
def mover_tablero(direccion):
    tablero = st.session_state.tablero
    index = tablero.index(0)
    fila, col = index // 3, index % 3

    if direccion == "Arriba" and fila > 0:
        nuevo_index = (fila-1)*3 + col
    elif direccion == "Abajo" and fila < 2:
        nuevo_index = (fila+1)*3 + col
    elif direccion == "Izquierda" and col > 0:
        nuevo_index = fila*3 + (col-1)
    elif direccion == "Derecha" and col < 2:
        nuevo_index = fila*3 + (col+1)
    else:
        return  # movimiento inválido

    tablero[index], tablero[nuevo_index] = tablero[nuevo_index], tablero[index]
    st.session_state.tablero = tablero

def mostrar_tablero_botones(tablero=None):
    if tablero is None:
        tablero = st.session_state.tablero
    for i in range(0,9,3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            valor = tablero[i+j]
            color = colores[valor]
            # Botón como ficha visual
            col.markdown(
                f"""
                <button style='width:60px; height:60px; font-size:28px; font-weight:bold; 
                background-color:{color}; border-radius:10px; border:2px solid black; cursor: default;'>
                {emojis[valor]}
                </button>
                """,
                unsafe_allow_html=True
            )

# =====================
# BFS para solución automática
# =====================
def bfs(inicial, objetivo):
    cola = deque([(inicial, [])])
    visitados = set()
    while cola:
        estado_actual, path = cola.popleft()
        if estado_actual == objetivo:
            return path
        visitados.add(tuple(estado_actual))
        index = estado_actual.index(0)
        fila, col = index // 3, index % 3
        direcciones = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in direcciones:
            nueva_fila, nueva_col = fila + dr, col + dc
            if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
                nuevo_index = nueva_fila*3 + nueva_col
                nuevo_estado = estado_actual.copy()
                nuevo_estado[index], nuevo_estado[nuevo_index] = nuevo_estado[nuevo_index], nuevo_estado[index]
                if tuple(nuevo_estado) not in visitados:
                    cola.append((nuevo_estado, path + [nuevo_estado]))
    return None

# Contenedor para animación
contenedor = st.empty()

# =====================
# Interfaz principal
# =====================
mostrar_tablero_botones()

st.subheader("Mover espacio vacío (⬜)")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Arriba", on_click=mover_tablero, args=("Arriba",))
with col2:
    st.button("Abajo", on_click=mover_tablero, args=("Abajo",))
with col3:
    st.button("Izquierda", on_click=mover_tablero, args=("Izquierda",))
st.button("Derecha", on_click=mover_tablero, args=("Derecha",))

# Botón para resolver automáticamente
if st.button("Resolver automáticamente"):
    solucion = bfs(st.session_state.tablero, estado_objetivo)
    if solucion:
        st.success(f"¡Solución encontrada en {len(solucion)} pasos!")
        for paso, estado in enumerate(solucion, start=1):
            contenedor.subheader(f"Paso {paso}")
            mostrar_tablero_botones(estado)
            time.sleep(0.5)
        st.session_state.tablero = estado_objetivo
    else:
        st.error("No se encontró solución")

# Comprobar si se resolvió manualmente
if st.session_state.tablero == estado_objetivo:
    st.success("¡Felicidades! Puzzle resuelto 🎉")

