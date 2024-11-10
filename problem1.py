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

# bellman_equation.value_iteration(states, 0.9, Move, make_move)
# bellman_equation.policy_iteration(states, 0.9, Move, make_move, origin_moves)
# bellman_equation.policy_iteration_truncate(states, 0.9, Move, make_move, origin_moves, steps=5)

if False:
    vi_results = bellman_equation.value_iteration(states, 0.9, Move, make_move)
    pi_results = bellman_equation.policy_iteration(states, 0.9, Move, make_move, origin_moves)
    pit_results = bellman_equation.policy_iteration_truncate(states, 0.9, Move, make_move, origin_moves, steps=2)

    print(pi_results)
    print(pit_results)
    print("=====================")
    plot_results([vi_results, pi_results, pit_results], ["value_iteration", "policy_iteration", "policy_iteration_truncate_2"], save_path="1.png")

if True:
    ground_truth = bellman_equation.policy_iteration_truncate(states, 0.9, Move, make_move, origin_moves, steps=1000)
    steps_set = [1, 5, 9, 56]
    pits = [bellman_equation.policy_iteration_truncate(states, 0.9, Move, make_move, origin_moves, steps=s) for s in steps_set]
    max_len = len(ground_truth)
    max_len = max(max_len, max([len(p) for p in pits]))
    ground_truth.extend([ground_truth[-1]] * (max_len - len(ground_truth)))
    for pit in pits:
        pit.extend([pit[-1]] * (max_len - len(pit)))
    for pit in pits:
        print(pit)
    pits = [
        [ground_truth[i] - pit[i] for i in range(max_len)]
        for pit in pits
    ]
    for i, s in enumerate(steps_set):
        print(pits[i])
        plot_results([pits[i]], [str(s)], save_path=f"diff_{s}.png")