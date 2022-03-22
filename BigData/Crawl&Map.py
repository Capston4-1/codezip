'''
# A single retrieve from data.go.kr
# Snapshot of the status of each charger
# run every 15 minutes on Linux

import requests
import datetime
import time

url = 'http://openapi.kepco.co.kr/service/EvInfoServiceV2/getEvSearchList'
params ={'serviceKey' : 'pzu8M6kHuMVoSmGMVoV8OFf4f7A0X1SgPoIf2PYEyM/z1+Yk5jEpkEmIE7yEkPlkyTO54QqOpnFdKQOucl5DvA==', 'pageNo' : '1', 'numOfRows' : '500', 'addr' : '제주' }

response = requests.get(url, params=params)
#print(response.content)

from bs4 import BeautifulSoup
wsoup = BeautifulSoup(response.text, 'html.parser')
res = wsoup.find_all('item')

#print(res)

cur= datetime.datetime.now()
print("Cur", cur)
cur1 = cur.strftime("%Y-%m-%d %H:%M:%S")
print("String1", cur)
cur = time.strptime(cur1, "%Y-%m-%d %H:%M:%S")
#print("String2", cur)
t1 = time.mktime(cur)

F= ['csId', 'cpId', 'cpstat']
mval = []
for n in res:
	flist = []
	tt = n.select_one('statUpdateDatetime')
	ts = tt.get_text()
#	print("Web", ts)
	ts = time.strptime(ts, "%Y-%m-%d %H:%M:%S")
#	print("String", ts)
	t2 = time.mktime(ts)
	dd = (t1-t2)//60
	print(dd)
	if (dd >=60):
		continue
	for i in range(len(F)):
		tt = n.select_one(F[i])	
		flist.append("'"+tt.get_text()+"'")
	flist.append("'"+cur1+"'")
#	print("insert into OpStatus values("+ ', '.join(flist) + ");")
	mval.append("("+ ', '.join(flist) + ")")

print("insert into OpStatus values", end='')
print(', '.join(mval)+";")
'''

'''
# Page 3. plot on the map with utilization colored 

import folium
f = open("./util.txt", 'r')

coor, util =[], []
while True:
	line = f.readline()
	if not line: break	
	f1, f2, f3 = map(float, line.split())
	coor.append([f2, f1])
	util.append(f3)
f.close()
#print(coor)
#print(util)

for i in range(len(util)):
	print(coor[i], util[i])

mx1, mx2 = coor[0][0], coor[0][0]
my1, my2 = coor[0][1], coor[0][1]
for i in range(1, len(coor)):
	mx1 = min([mx1, coor[i][0]])
	mx2 = max([mx1, coor[i][0]])
	my1 = min([my1, coor[i][1]])
	my2 = max([my1, coor[i][1]])
mxc, myc = (mx1+mx2) / 2, (my1+my2)/2
print(mxc, myc)
ttip =['may be failed', 'low', 'middle', 'hot']
m = folium.Map([mxc, myc], zoom_start=10)
for i in range(len(coor)):
	if (util[i]< 0.05):
    		folium.Marker(coor[i], icon=folium.Icon(color = 'darkblue'), tooltip = ttip[0] ).add_to(m)
	elif (util[i]< 0.20):
    		folium.Marker(coor[i], icon=folium.Icon(color = 'lightblue'),  tooltip = ttip[1]).add_to(m)
	elif (util[i]< 0.40):
    		folium.Marker(coor[i], icon=folium.Icon(color = 'orange'),  tooltip = ttip[2]).add_to(m)
	else:
    		folium.Marker(coor[i], icon=folium.Icon(color = 'red'),  tooltip = ttip[3]).add_to(m)

m.save('./map.html')
'''


