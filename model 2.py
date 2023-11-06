import math
import random
import numpy as np
from collections import Counter
import pandas as pd
from sympy import *

# 设立传播范围：
ran = 10

# 设立传播时间：
spr = 10

# 设立救援队到达时间
arv = 30

# 设立救援队救一颗树的时间/会瞬移
save = 3

# 设立各项金额
c1 = 50
c2 = 10
c3 = 100
# 导入生成森林数据
x = np.loadtxt('./forest.csv')
y = np.loadtxt('./forest1.csv')

# t_all = np.zeros((21, 10))
# money_all = np.zeros((21, 10))
# 选取不同的着火点
# for kk in range(10):
for kk in range(6,7):
    # random.seed(kk)
    # tree = random.randint(0, 499)
    tree = 201
    print(tree)
    # 设立汪汪救援队人数
    for k in range(1):
    # for k in range(15, 16):

        # 设立每棵树的状态，0=未着火，1=即将着火，2=正在着火，3=已烧焦，4=被熄灭
        state = [0]*500

        # 随机挑选一颗幸运树进行点燃
        state[tree] = 2
        change = [0]*500
        # 着火时间倒计时
        fire = [0]*500
        fire[tree] = 30
        # 起火倒计时
        time = [0]*500
        # 总时长
        t = 0
        # 建模
        # 当仍有树状态为着火时循环
        while not (np.array(state) != 2).all():
            print(t)
            # 每次时钟走1分钟
            t = t + 1
            for i in range(500):
                if change[i] == 0:
                    if state[i] == 2:
                        # 燃烧十分钟烧焦
                        if fire[i] > 0:
                            fire[i] = fire[i] - 1
                        elif fire[i] <= 0:
                            state[i] = 3
                        for j in range(500):
                            if state[j] == 0:
                                aij = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5
                                cos_x = (y[j] - y[i])/aij
                                sin_x = (x[j] - x[i])/aij
                                aa = 1/4*cos_x + (3 ** 0.5)/4 * sin_x
                                if 3.14 / (exp(aij / 3.14)) + aa > 0 and (aa * exp(aij) + 3.14) / (aa + 3.14) > 0:
                                    time[j] = 3.14 / aa * math.log((aa * exp(aij) + 3.14) / (aa + 3.14), math.e)
                                    change[j] = 1
                                    state[j] = 1
                            if state[j] == 1:
                                aij = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5
                                cos_x = (y[j] - y[i]) / aij
                                sin_x = (x[j] - x[i]) / aij
                                aa = 1 / 4 * cos_x + (3 ** 0.5) / 4 * sin_x
                                if 3.14 * 1 / (math.e ** (aij / 3.14)) + aa > 0 and (aa * exp(aij) + 3.14) / (aa + 3.14) > 0:
                                    time_f = 3.14 / aa * math.log(aa * exp(aij) + 3.14, math.e)
                                    if time[j] > time_f:
                                        time[j] = time_f
                                        change[j] = 1
                    elif state[i] == 1:
                        # 起火倒计时结束开始起火
                        if time[i] > 0:
                            time[i] = time[i] - 1
                        if time[i] <= 0:
                            state[i] = 2
                            fire[i] = 30

                elif change[i] == 1:
                    change[i] = 0
            # 30分钟后救援队到来，每人每3分钟灭一颗树
            if (t >= arv) & ((t - arv) % save == 0) & (k != 0):
                extinguish = np.asarray(fire).argsort()[-k:]
                for i in extinguish:
                    if fire[i] > 0:
                        fire[i] = 0
                        state[i] = 4
                        for j in range(500):
                            if (state[j] == 1) & (((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 <= ran):
                                flag = 0
                                for l in range(500):
                                    if((x[l] - x[j]) ** 2 + (y[l] - y[j]) ** 2) ** 0.5 <= ran:
                                        if state[l] == 2:
                                            flag = 1
                                if flag == 0:
                                    state[j] = 0
                                    time[j] = 0

        print('人数：' + str(k))
        print('时间：' + str(t))
        print(Counter(state))
        print('金额：' + str((state.count(3)+state.count(4))*c1 + state.count(4) * c2 + k * c3))
        print('')
        # print(kk, k)
        # t_all[k][kk] = t
        # money_all[k][kk] = (state.count(3) + state.count(4)) * c1 + state.count(4) * c2 + k * c3

# print(t_all)
# print(money_all)
print(state)
# data1 = pd.DataFrame(t_all)
# data2 = pd.DataFrame(money_all)
# data1.to_csv('t.csv')
# data2.to_csv('m.csv')
