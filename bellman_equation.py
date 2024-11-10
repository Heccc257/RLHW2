import numpy as np
from policy import *
from tqdm import tqdm

def policy_evaluation(r, gamma, P, v):
    """
    策略评估
    :param rpi: 收益矩阵
    :param Ppi: 转移概率矩阵
    :param theta: 收敛阈值
    """
    v = r + gamma * np.dot(P, v)
    return v
def policy_evaluate_truncated(r, gamma, P, v, steps, theta=1e-3):
    for _ in range(steps):
        v_new = policy_evaluation(r, gamma, P, v)
        if np.linalg.norm(v_new - v) < theta:
            break
        v = v_new
    return v

def policy_improvement(states, gamma, v, Move, make_move):

    """
    策略改进
    :param rpi: 收益矩阵
    :param Ppi: 转移概率矩阵
    :param v: 策略评估结果
    """
    P = np.zeros((len(states), len(states)))
    R = np.zeros(len(states))
    pi = {}

    for s in states:
        max_val = -np.inf
        best_nxt_stat = -1
        for m in Move:
            nxt_stat, r = make_move(s, m)
            if r + gamma * v[nxt_stat.id] > max_val:
                max_val = r + gamma * v[nxt_stat.id]
                best_nxt_stat = nxt_stat
                R[s.id] = r
                pi[s] = m
        
        P[s.id, best_nxt_stat.id] = 1
    return P, R, pi


def debugV(v):
    for i in range(5):
        print(v[i*5:(i+1)*5])
def value_iteration(states, gamma, Move, make_move, theta=1e-3):
    results = []
    epoch = 1000
    v = np.zeros(len(states))
    for i in range(epoch):
        P, R, pi = policy_improvement(states, gamma, v, Move, make_move)
        v_new = policy_evaluation(R, gamma, P, v)
        if np.linalg.norm(v_new - v) < theta:
            break
        # print(i)
        # debugV(v)
        v = v_new
        results.append(float(v[2]))
    return results

def policy_iteration(states, gamma, Move, make_move, moves_init, theta=1e-3):
    results = []
    epoch = 1000
    v = np.zeros(len(states))
    P, R = extract_policy(states, moves_init, make_move)

    for i in range(epoch):
        # 达到收敛
        v_new = policy_evaluate_truncated(R, gamma, P, v, steps=1000)
        if np.linalg.norm(v_new - v) < theta:
            break
        v = v_new
        results.append(float(v[2]))
        P, R, pi = policy_improvement(states, gamma, v, Move, make_move)
        print(i)
        debugV(v)
        print(P)
    
    return results

def policy_iteration_truncate(states, gamma, Move, make_move, moves_init, steps, theta=1e-3):
    results = []
    epoch = 1000
    v = np.zeros(len(states))
    P, R = extract_policy(states, moves_init, make_move)

    for i in range(epoch):
        # 达到收敛
        v_new = policy_evaluate_truncated(R, gamma, P, v, steps=steps)
        if np.linalg.norm(v_new - v) < theta:
            break
        v = v_new
        results.append(float(v[2]))
        P, R, pi = policy_improvement(states, gamma, v, Move, make_move)
    return results