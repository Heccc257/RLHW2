import numpy as np
from policy import *
from tqdm import tqdm
import random

class AverageArray:
    def __init__(self):
        self.sum = 0.0
        self.cnt = 0
    def append(self, g):
        self.sum += g
        self.cnt += 1
    def average(self):
        return self.sum / self.cnt

class Value():
    def __init__(self, Move, epsilon):
        self.values = {}
        for move in Move:
            self.values[move] = 0
        self.e = epsilon
        pass
    def get_pi(self):
        pi = {}
        a_star = max(self.values, key=self.values.get)
        tot = len(self.values.keys())
        for move in self.values.keys():
            if move == a_star:
                pi[move] = 1 - (tot - 1.0) / tot * self.epsilon
            else:
                pi[move] = 1.0 / tot * self.epsilon
        return pi
    def evaluate(a, v):
        self.values[a] = v

def policy_evaluation(r, gamma, P, v):
    """
    策略评估
    :param rpi: 收益矩阵
    :param Ppi: 转移概率矩阵
    :param theta: 收敛阈值
    """
    v = r + gamma * np.dot(P, v)
    return v

def choose_move(s: State, pi):
    pro = pi[s]
    return random.choices(list(pro.keys()), list(pro.values()), k=1)[0]

def make_episode(states, Move, pi, T, make_move):
    """
    生成一个episode
    :param states: 状态集合
    :param Move: 动作集合
    :param pi: 策略
    :param T: 最大步数
    :param make_move: 动作函数
    """

    s = random.choice(states)
    a = random.choice(list(Move))
    episode = []
    for i in range(T):
        s_nxt, r = make_move(s, a)
        a_nxt = choose_move(s_nxt, pi)
        episode.append((s, a, r))
        s, a = s_nxt, a_nxt
    return episode



def policy_evaluation(s, a, returns):
    return returns[s, a]

def every_visit(st, at, g, returns, q):
    returns[st, at].append(g)

    q[st].evaluate
