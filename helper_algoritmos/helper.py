import numpy as np
import random


# Q-Learning
def inicializar_Q(nS, nA, tipo='ones'):
    Q = {}
    for i in range(nS):
        if tipo == 'ones':
            Q[i] = [1.0] * nA
        else:
            Q[i] = [random.random() for _ in range(nA)]
    return Q

def e_greedy(s, Q, epsilon, nA):
    if np.random.rand() >= epsilon:
        accion = np.argmax(Q[s])
    else:
        accion = np.random.randint(0, nA)
    return accion

def move_and_reward(state, action, labyrinth, rows, cols):
    x, y = state // cols, state % cols
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
    dx, dy = moves[action]
    nx, ny = x + dx, y + dy

    if 0 <= nx < rows and 0 <= ny < cols:  # Verificar límites del laberinto
        next_state = nx * cols + ny
        if labyrinth[nx][ny] == 1:  # Celda bloqueada
            return state, -50, True
        elif nx == rows - 1 and ny == cols - 1:  # Meta
            return next_state, 50, True
        else:  # Movimiento válido
            return next_state, 0, False
    return state, -1, False  # Movimiento inválido