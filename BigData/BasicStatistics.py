'''
# 1. daily number of active chargers and that of reports
# figure on page 6
from datetime import date
f = open("./Data/dayactive.txt", 'r')

D, A, R =[], [], []	# Date, Active, Reports
Db = date(2021, 12, 7)
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2, f3 = line.split()
#	D.append(f1)
	yy, mm, dd = map(int, f1.split('-'))
	dd = date(yy,mm, dd)- Db
	D.append(dd.days)
	A.append(int(f2))
	R.append(int(f3))

for i in range(len(R)):
	R[i] = R[i]/100
import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(D, A, marker='o', color='red', linestyle='-', label='Active')
ax1.plot(D, R, marker='+', color='green', linestyle='-', label='Reports')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Daily operations')
ax1.set_ylim([0, 250])

plt.xlabel('Day')
plt.ylabel('Number of active chargers/reports(*100)')
#plt.xticks(list(range(0,18)),['7(T)','','','','','12(S)','','','','','','','19(S)','','','','','24(F)'])
#K = list(map(str, K))
#plt.xticks(K)
plt.legend(loc='best')
plt.show()
'''

'''
# 2. daily all-region utilization
# plot on page 6
from datetime import date
f = open("./Data/dayutil.txt", 'r')
Db = date(2021, 12, 7)

D, U=[], []	# Date, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2 = line.split()
	yy, mm, dd = map(int, f1.split('-'))
	dd = date(yy,mm, dd)- Db
	D.append(dd.days)
	U.append(float(f2))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
#ax1.plot(D, U, marker='o', color='red', linestyle='-', label='Active')
ax1.bar (D, U, align='center', color='green')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Daily utilization')
ax1.set_ylim([0, 0.4])

plt.xlabel('Day')
plt.ylabel('Utilization')
#plt.xticks(list(range(0,18)),['7(T)','','','','','12(S)','','','','','','','19(S)','','','','','24(F)'])
#K = list(map(str, K))
#plt.xticks(K)
plt.legend(loc='best')
plt.show()
'''

'''
# 3. seasonal decomposition
# plot on page 7
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import matplotlib.pyplot as plt
f = open("./Data/dayutil.txt", 'r')

D, U=[], []	# Date, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2 = line.split()
	U.append(float(f2))
	D.append(f1)

df = pd.DataFrame(U)
df.index =pd.to_datetime(D)

dec = seasonal_decompose(U, model='additive', period=7)
plt.rcParams['figure.figsize'] = [12, 6]

print(dec.resid)
print(dec.seasonal)

dec.plot()
plt.show()
'''

'''
# 4. hourly all-region utilization
# plot on page 8
f = open("./Data/hourly.txt", 'r')

D, U=[], []	# Date, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2 = line.split()
	D.append(f1)
	U.append(float(f2))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(U, marker='o', color='red', linestyle='-', label='Active')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Hourly utilization')
ax1.set_ylim([0, 0.5])

plt.xlabel('Hour-of-day')
plt.ylabel('Utilization')

plt.legend(loc='best')
plt.show()
'''

'''
# 5. Effect of day-of-week
# plot on page 8
f = open("./Data/wday.txt", 'r')

D, U=[], []	# Date, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2 = line.split()
	D.append(f1)
	U.append(float(f2))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(U, marker='o', color='red', linestyle='-', label='Utilization')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Day-of-week utilization')
ax1.set_ylim([0, 0.5])

plt.xlabel('Day-of-week')
plt.ylabel('Utilization')
plt.xticks(list(range(0,7)),['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

plt.legend(loc='best')
plt.show()


'''
# 6. charger-by-charger utilization - Line plot
# plot on page 9
f = open("./Data/chargerutil.txt", 'r')

S, C, U=[], [], []		# Station, Charger, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2, f3 = line.split()
	if (f3=='NULL'):
		continue
	S.append(f1)
	C.append(f2)
	U.append(float(f3))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(U, marker='o', color='red', linestyle='-', label='Utilization')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Charger-by-charger utilization')
ax1.set_ylim([0, 0.8])

plt.xlabel('Charger')
plt.ylabel('Utilization')
plt.legend(loc='best')
plt.show()
'''

'''
# 7. charger-by-charger utilization - Histogram
# plot on page 9
f = open("./Data/chargerutil.txt", 'r')

S, C, U=[], [], []		# Station, Charger, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2, f3 = line.split()
	if (f3=='NULL'):
		continue
	S.append(f1)
	C.append(f2)
	U.append(float(f3))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig =plt.figure()
ax1 = fig.add_subplot(1,1,1)
n, bins, patches = ax1.hist(U, bins=25, density=False, color='orange', alpha=0.5)

ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

plt.xlabel('Bins')
plt.ylabel('Number of values in Bin')
fig.suptitle('Histograms', fontsize=14, fontweight='bold')
ax1.set_title('Density distribution')
plt.show()
'''

'''
# 8. charger-by-charger houlry utilization - Line plot
# plot on page 10
f = open("./Data/sch.txt", 'r')

S, C, H, U=[], [], [], []		# Station, Charger, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2, f3, f4 = line.split()
	if (f4=='NULL'):
		continue
	S.append(f1)
	C.append(f2)
	H.append(int(f3))
	U.append(float(f4))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.plot(U, marker='o', color='red', linestyle='-', label='Utilization')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_title('Charger-Hour utilization')
ax1.set_ylim([0, 1.0])

plt.xlabel('Charger-hour')
plt.ylabel('Utilization')
#plt.xticks(list(range(0,18)),['7(T)','','','','','12(S)','','','','','','','19(S)','','','','','24(F)'])
#K = list(map(str, K))
#plt.xticks(K)
plt.legend(loc='best')
plt.show()
'''

'''
# 9. charger-by-charger houlry utilization - Histogram
# plot on page 10
f = open("./Data/sch.txt", 'r')

S, C, H, U=[], [], [], []		# Station, Charger, Utilization
line = f.readline()
while True:
	line = f.readline()
	if not line: 
		break
	f1, f2, f3, f4 = line.split()
	if (f4=='NULL'):
		continue
	S.append(f1)
	C.append(f2)
	H.append(int(f3))
	U.append(float(f4))

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

fig =plt.figure()
ax1 = fig.add_subplot(1,1,1)
n, bins, patches = ax1.hist(U, bins=30, density=False, color='orange', alpha=0.5)

ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

plt.xlabel('Bins')
plt.ylabel('Number of values in Bin')
fig.suptitle('Histograms', fontsize=14, fontweight='bold')
ax1.set_title('Density distribution')
plt.show()
'''



