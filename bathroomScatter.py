import datetime
import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3 as lite

#Plotly signin info
py.sign_in(user, key)

#Arrays for holding data
bath1Hour=[]
bath2Hour=[]
timeSpent1=[]
timeSpent2=[]

#Database Connection
con = lite.connect('bathroom.db')
with con:
	#Bathroom1 query
	cur = con.cursor()
	inputString = "select * from bath WHERE date(datetime(Time, 'unixepoch', 'localtime')) AND Bathroom=1"
	cur.execute(inputString)
	results = cur.fetchall()
	time1 = [x[1] for x in results]
	for x in time1:
		value = datetime.datetime.fromtimestamp(x)
		hour = value.strftime('%H:%M:%S')
		bath1Hour.append(value)
	count1 = [x[2] for x in results]
	for x in count1:
		#Divide seconds occupied by 60 to get minutes
		timeSpent1.append((float(x))/60)
	
	#Bathroom 2 query	
	cur2 = con.cursor()
	inputString = "select * from bath WHERE date(datetime(Time, 'unixepoch', 'localtime')) AND Bathroom=2"
	cur2.execute(inputString)
	results = cur2.fetchall()
	time2 = [x[1] for x in results]
	for x in time2:
		value = datetime.datetime.fromtimestamp(x)
		hour = value.strftime('%H:%M:%S')
		bath2Hour.append(value)
	count2 = [x[2] for x in results]
	for x in count2:
		timeSpent2.append((float(x))/60)


Bathroom1 = Scatter(
    x=bath1Hour,
    y=timeSpent1,
    mode='markers',
    name="Bathroom1",
    marker=Marker(
        color='rgb(102, 153, 255)'
    )
)
Bathroom2 = Scatter(
    x=bath2Hour,
    y=timeSpent2,
    name="Bathroom2",
    mode='markers',
    marker=Marker(
        color='rgb(255, 102, 0)'
    )
)
data = Data([Bathroom1, Bathroom2])
layout = Layout(
    showlegend=False,
    title='Bathroom Scatter Plot',
    xaxis=XAxis(title='Time'),
    yaxis=YAxis(title='Time in Bathroom (Min)')
)
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig, filename='scatterbars')
