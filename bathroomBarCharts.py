import datetime
import plotly.plotly as py
import sqlite3 as lite
from plotly.graph_objs import *

#Plotly signin info
py.sign_in(user, key)

#Arrays for holding data
bath1Hour=[]
bath2Hour=[]

#Database connection
con = lite.connect('bathroom.db')
with con:
	cur = con.cursor()
	inputString = "select * from bath WHERE date(datetime(Time, 'unixepoch', 'localtime')) = date('now', 'localtime') AND Bathroom=1"
	cur.execute(inputString)
	results = cur.fetchall()
	time1 = [x[1] for x in results]
	for x in time1:
		value = datetime.datetime.fromtimestamp(x)
		hour = value.strftime('%H:%M:%S')
		bath1Hour.append(value)

	cur2 = con.cursor()
	inputString = "select * from bath WHERE date(datetime(Time, 'unixepoch', 'localtime')) = date('now', 'localtime' ) AND Bathroom=2"
	cur2.execute(inputString)
	results = cur2.fetchall()
	time2 = [x[1] for x in results]
	for x in time2:
		value = datetime.datetime.fromtimestamp(x)
		hour = value.strftime('%H:%M:%S')
		bath2Hour.append(value)

	
#Set histogram view to automatically group plot points
trace1 = Histogram(
    x=bath1Hour,
    name="Bathroom1", 
            nbinsx=40, #this sets the amount of bins of grouped data
)
trace2 = Histogram(
    x=bath2Hour,
    name='Bathroom2',
    nbinsx=40,
)
data = Data([trace1, trace2])
layout = Layout(
    barmode='group',
    bargroupgap=0,
    title="Bathroom Use",
    xaxis=XAxis(title='Time'),
    yaxis=YAxis(title='Number of Uses')
)
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig, filename='grouped-bar')
