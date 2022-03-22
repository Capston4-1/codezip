# ------------------------------------------------------------------------
# Distance effect analysis and Artificial Neural Network Model
# ------------------------------------------------------------------------

'''
# 충전소당 보유 충전기 수
# plot on page 5
import math
import matplotlib.pyplot as plt
plt.style.use('ggplot')

f = open("./Data/loc.txt", 'r')

dic ={}
line = f.readline()
C, U=[],[]
while True:
	line = f.readline()
	if not line: 
		break
	ff = line.split()
	U.append(float(ff[5]))
	if ((ff[3] in dic) == False):
		dic[ff[3]] =1
	else:
		dic[ff[3]] = dic[ff[3]]+1

# number of chargers per station
C=list(dic.values())
C.sort(reverse=True)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(C, marker='o', color='red', linestyle='-', label='# of chargers')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Number of chargers per station')
#ax1.set_ylim([0, 0.5])

plt.xlabel('Stations')
plt.ylabel('Number of chargers')
plt.legend(loc='best')
plt.show()
'''

'''
# 가장 가까운 충전기의 사용율과의 상관관계
# plot on page 5

import math
import matplotlib.pyplot as plt

def dist(c1, c2):
	dx = (c1[0]-c2[0])*31* 3.6
	dy = (c1[1]-c2[1])*27 * 3.6
	dd = math.sqrt(dx*dx+dy*dy)
#	if (dd==0):
#		print(c1[0], c1[1], c2[0], c2[1])
	return dd

plt.style.use('ggplot')
f = open("./Data/loc.txt", 'r')
dic ={}
line = f.readline()
C, U=[],[]

while True:
	line = f.readline()
	if not line: 
		break
	ff = line.split()
	C.append([float(ff[0]), float(ff[1])])
	U.append(float(ff[5]))

L = len(C)
dd =[]
for i in range(L):
	d=[]
	for j in range(L):
		d.append(round(dist(C[i], C[j]), 5))
	dd.append(d)

u = 0
R =[]
for i in range(L):
	dd[i][i] = 1000000
	mm = 1000000
	for j in range(L):
		if (mm > dd[i][j]):
			mm = dd[i][j]
	loc = dd[i].index(mm)
	R.append(U[loc])
#	print(i, mm, U[i], U[loc] )

# Correlation library
import numpy as np
print(np.corrcoef(U, R))

print(min(U), max(U), min(R), max(R))
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(U, R, marker='o', color='red', linestyle='-', label='Utilization')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Nearby station utilization')
ax1.set_ylim([0, 0.7])

plt.xlabel('Utilization')
plt.ylabel('Nearby station utilization')
plt.legend(loc='best')
plt.show()
'''

'''
# plot on page 11
# 인공신경망 기반으로 예측 모델을 만든다.
# 시계열처럼 생각하여 4일 동안의 사용율을 기반으로 내일 거를 예측한다.
# 입력 (이전 4일의 사용율 + 요일), 출력 : 내일의 사용율
# Y = F(X1, X2, ...Xn)

import math
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import mglearn

f = open("./Data/dayutil.txt", 'r')
line = f.readline()
D =[]
st = date(2021, 12, 7)
while True:
	line = f.readline()
	if not line: 
		break
	ff = line.split()
	yy, mm, dd = map(int, ff[0].split('-'))
	dd = date(yy,mm,dd) - st
	D.append([dd.days, float(ff[1])])

# 빈 날짜는 가장 최근 사용율로 채움
# 학습을 위해서는 Y가 정수가 되어야 함
U=[]
U.append(D[0][1])
for i in range(1, len(D)):
	for j in range(D[i][0] - D[i-1][0]-1):
		U.append(int(D[i-1][1]*1000))
	U.append(int(D[i][1]*1000))


X, Y = [], []
for i in range(len(U)-4):
# 요일이 들어간 학습
#	t = U[i:i+4]
#	t.append(i%7)
#	X.append(t)
# 요일이 들어가지 않은 학습
	X.append(U[i:i+4])
	Y.append(U[i+4])

x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=42)
#print(x_train, y_train)
#print(len(x_train), len(y_train), len(X), len(Y))

mlp = MLPClassifier(random_state=42, hidden_layer_sizes=[10], max_iter=5000)
mlp.fit(x_train, y_train)

# 예측값이 정확히 일치하는지 검사하는 것이므로 무의미
print("fitting score", mlp.score(x_train, y_train))
print("predicting score", mlp.score(x_test, y_test))

# Root mean square error 
def Rmse(a, b):
	ss = 0
	for i in range(len(a)):
		ss += (a[i]-b[i]) * (a[i]-b[i])
	return(math.sqrt(ss/len(a)))

pr = mlp.predict(x_test)	# 학습에 사용되지 않은 데이터
print('test')
print(pr)

# 예측 결과인 pr은 lvalue로 못 쓰이나봐..
# pr[i] = pr[i]/1000로 했더니 다 0이 되네..
P=[]
for i in range(len(y_test)):
	y_test[i]= y_test[i]/1000
	P.append(pr[i]/1000)
print('test', Rmse(P, y_test))

pr = mlp.predict(X)		# 모든 데이터
print('All')
print(pr)
print(Y)

P=[]
for i in range(len(Y)):
	Y[i] = Y[i]/1000
	P.append(pr[i]/1000)
print('all', Rmse(P, Y))

print('after')
print(P)
print(Y)

plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(Y, marker=r'o', color=u'green', linestyle='-', label='actual')
ax1.plot(P, marker=r'+', color=u'red', linestyle='--', label='predicted')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_ylim([0, 0.3])

plt.xlabel('Day')
plt.ylabel('Utilization')
plt.legend(loc='best')
plt.show()
'''
