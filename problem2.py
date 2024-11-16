from enum import Enum
from policy import *
from typing import Tuple
import bellman_equation
import math

# import plot_graph
import matplotlib.pyplot as plt
def plot_results(lines, labels, save_path):
    plt.figure(figsize=(10, 6))
    optimal_value = 0
    for line, label in zip(lines, labels):
        # print(line, label)
        x = range(len(line))
        plt.plot(x, line, label=label)
        optimal_value = max(optimal_value, max(line))
    plt.axhline(y=optimal_value, color='r', linestyle='--', linewidth=2)
    plt.legend()
    plt.savefig(save_path)

N = 5
state_id = {}
coordinate = {}
for i in range(N):
    for j in range(N):
        state_id[(i, j)] = i*5 + j
        coordinate[i*5 + j] = (i, j)
states = [State(i*N + j, i, j) for i in range(N) for j in range(N)]

r_init = np.array([
    [0, 0, 0, 0, 0],
    [0, -10, -10, 0, 0],
    [0, 0, -10, 0, 0],
    [0, -10, 1, -10, 0],
    [0, -10, 0, 0, 0],
])

class Move(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    STAY = (0, 0)

def make_move(s: State, a: Move) -> Tuple[State, float]:
    """
    执行动作，返回下一个状态和奖励
    :param s: 当前状态
    :param a: 动作
    :return: 下一个状态和奖励
    """
    tgt = (s.coor[0] + a.value[0], s.coor[1] + a.value[1])

    if tgt[0] < 0 or tgt[0] >= N or tgt[1] < 0 or tgt[1] >= N:
        # out of boundary
        return s, -1
    else:
        return State(state_id[tgt], tgt[0], tgt[1]), r_init[tgt[0]][tgt[1]]

origin_moves = [[Move.STAY for _ in range(N)] for _ in range(N)]
print(origin_moves)