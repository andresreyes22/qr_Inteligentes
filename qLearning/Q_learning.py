# pylint: disable=no-member
import numpy as np
from helper_algoritmos.helper import inicializar_Q, e_greedy, move_and_reward

def aplicarQlearning(labyrinth,  alpha=0.4, gamma=0.999, epsilon=0.1, K=2000):
    rows, cols = len(labyrinth), len(labyrinth[0])
    nS = rows * cols
    nA = 4  # Número de acciones (arriba, abajo, izquierda, derecha)
    Q = inicializar_Q(nS, nA)
    retorno = []

    for episodio in range(K):
        retorno_acumulado = 0
        state = 0  # Estado inicial (siempre la esquina superior izquierda)
        action = e_greedy(state, Q, epsilon, nA)  # Seleccionar acción
        done = False

        while not done:   
            next_state, reward, done = move_and_reward(state, action, labyrinth, rows, cols)
            next_action = np.argmax(Q[next_state])
            retorno_acumulado += reward

            if not done:
                Q[state][action] += alpha * (reward + gamma * Q[next_state][next_action] - Q[state][action])
            else:
                Q[state][action] += alpha * (reward - Q[state][action])

            state, action = next_state, next_action

        retorno.append(retorno_acumulado)

    return Q, retorno

