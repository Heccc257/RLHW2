import numpy as np
from policy import *
from tqdm import tqdm
import random

def policy_evaluation(r, gamma, P, v):
    """
    策略评估
    :param rpi: 收益矩阵
    :param Ppi: 转移概率矩阵
    :param theta: 收敛阈值
    """
    v = r + gamma * np.dot(P, v)
    return v

def choose_move(s: State. pi):
    pro = pi[S]
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
        a_nxt = choose_move(s_nxt)
        episode.append((s, a, r))
        s, a = s_nxt, a_nxt
    return episode

def policy_evaluation(s, a, returns):
    return resturns[s, a]
        
def policy_improvement(states, gamma, v, Move, make_move, episode):
    T = len(episode)
    g = 0
    for i in range(T-1, 0, -1):
        s, a, r = episode[i]
        g = gamma * g + r
