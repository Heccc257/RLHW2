import numpy as np
from enum import Enum
from typing import Tuple

class State:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.coor = (x, y)

def extract_policy(S, moves: list, make_move):
    policy = np.zeros((len(S), len(S)), dtype=int)
    rpi = np.zeros(len(S), dtype=float)
    for s in S:
        nxt_stat, r = make_move(s, moves[s.coor[0]][s.coor[1]])

        policy[s.id, nxt_stat.id] = 1
        rpi[s.id] = r

    return policy, rpi

def extract_policy_from_pi(states, pi, make_move):
    """
    根据策略，提取转移概率矩阵和收益矩阵
    :param states: 状态集合
    :param pi: 策略
    :param make_move: 动作函数
    :return: 转移概率矩阵和收益矩阵
    """
    P = np.zeros((len(states), len(states)))
    rpi = np.zeros(len(states))
    for s in states:
        nxt_stat, r = make_move(s, pi[s])
        P[s.id, nxt_stat.id] = 1
        rpi[s.id] = r
    
    return rpi, P