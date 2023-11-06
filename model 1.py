import random
import numpy as np
from collections import Counter
import pandas as pd

# 设立传播范围：
ran = 10

# 设立传播时间：
spr = 10

# 设立救援队到达时间
arv = 0

# 设立救援队救一颗树的时间/会瞬移
save = 3

# 设立各项金额
c1 = 50
c2 = 10
c3 = 100
# 导入生成森林数据
x = []
y = []
for i in range(-50, 51, 5):
    for j in range(21):
        x.append(i)

for j in range(21):
    for i in range(-50, 51, 5):
        y.append(i)

print(x[220])
print(y[220])
t_all = np.zeros((21, 10))
money_all = np.zeros((21, 10))
time_0 = []
# 选取不同的着火点
for kk in range(1):
    tree = 220
    # 设立汪汪救援队人数
    for k in range(31):
    # for k in range(15, 16):

        # 设立每棵树的状态，0=未着火，1=即将着火，2=正在着火，3=已烧焦，4=被熄灭
        state = [0]*441

        # 随机挑选一颗幸运树进行点燃
        state[tree] = 2
        change = [0]*441
        # 着火时间倒计时
        fire = [0]*441
        fire[tree] = 10
        # 起火倒计时
        time = [0]*441
        # 总时长
        t = 0
        # 建模
        # 当仍有树状态为着火时循环
        while not (np.array(state) != 2).all():
            # 每次时钟走0.1分钟
            t = t + 1
            for i in range(441):
                if change[i] == 0:
                    if state[i] == 2:
                        # 燃烧十分钟烧焦
                        if fire[i] > 0:
                            fire[i] = fire[i] - 1
                        elif fire[i] <= 0:
                            state[i] = 3
                        for j in range(441):
                            if state[j] == 0:
                                # 欧氏距离小于10的点会被引燃
                                if ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 <= ran:
                                    time[j] = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 / ran * spr
                                    state[j] = 1
                                    change[j] = 1
                            if state[j] == 1:
                                if ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 <= ran:
                                    if time[j] > ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 / ran * spr:
                                        time[j] = ((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 / ran * spr
                    elif state[i] == 1:
                        # 起火倒计时结束开始起火
                        if time[i] > 0:
                            time[i] = time[i] - 1
                        if time[i] <= 0:
                            state[i] = 2
                            fire[i] = 10

                elif change[i] == 1:
                    change[i] = 0
            # 30分钟后救援队到来，每人每3分钟灭一颗树
            if (t >= arv) & ((t - arv) % save == 0) & (k != 0):
                extinguish = np.asarray(fire).argsort()[-k:]
                for i in extinguish:
                    if fire[i] > 0:
                        fire[i] = 0
                        state[i] = 4
                        for j in range(441):
                            if (state[j] == 1) & (((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) ** 0.5 <= ran):
                                flag = 0
                                for l in range(441):
                                    if((x[l] - x[j]) ** 2 + (y[l] - y[j]) ** 2) ** 0.5 <= ran:
                                        if state[l] == 2:
                                            flag = 1
                                if flag == 0:
                                    state[j] = 0
                                    time[j] = 0
            time_0.append(state.count(3)+state.count(2))
        print('人数：' + str(k))
        print('时间：' + str(t))
        # print(time)
        # print(state)
        # print(Counter(state))
        print('金额：' + str((state.count(3)+state.count(4))*c1 + state.count(4) * c2 + k * c3))
        print('')
        # print(kk, k)
        # t_all[k][kk] = t
        # money_all[k][kk] = (state.count(3) + state.count(4)) * c1 + state.count(4) * c2 + k * c3

# print(t_all)
# print(money_all)

# data1 = pd.DataFrame(t_all)
# data2 = pd.DataFrame(money_all)
# data1.to_csv('t.csv')
# data2.to_csv('m.csv')
# print(t)
# print(time_0)
# dataframe = pd.DataFrame({'': time_0})
# dataframe.to_csv("test3.csv", index=False, sep=',')
