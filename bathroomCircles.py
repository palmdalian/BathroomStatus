import datetime
import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3 as lite

#sign in for plot.ly
py.sign_in(user, key)

#Arrays to hold sql results
bath1Hour=[]
bath2Hour=[]
bathNumber=[]
bathNumber2=[]
size1=[]
size2=[]

#Sqlite Connection
con = lite.connect('bathroom.db')
with con:
	#Bathroom1 Cursor
	cur = con.cursor()
	inputString = "select * from bath WHERE Bathroom=1"
	cur.execute(inputString)
	results = cur.fetchall()
	time1 = [x[1] for x in results]
	for x in time1:
		#Get date/time stored in database
		value = datetime.datetime.fromtimestamp(x)
		bath1Hour.append(value)
		#Set the bathroom number in array every time there's a new entry. Makes plotting easier.
		bathNumber.append("1")
		
	#Get the number of seconds bathroom was occupied
	count1 = [x[2] for x in results]
	for x in count1:
		#Divide by 10 to make the circles more manageable
		size1.append((float(x))/10)
	
	#Bathroom2 Cursor	
	cur2 = con.cursor()
	inputString = "select * from bath WHERE Bathroom=2"
	cur2.execute(inputString)
	results = cur2.fetchall()
	time2 = [x[1] for x in results]
	for x in time2:
		value = datetime.datetime.fromtimestamp(x)
		bath2Hour.append(value)
		bathNumber2.append("2")
	count2 = [x[2] for x in results]
	for x in count2:
		size2.append((float(x))/10)


#Setting Data for plotly
Bathroom1 = Scatter(
    x=bath1Hour,
    y=bathNumber,
    mode='markers',
    name='Bathroom1',
    marker=Marker(
        color='rgb(102, 153, 255)',
        size=size1,
        opacity=0.6
    )
)
Bathroom2 = Scatter(
    x=bath2Hour,
    y=bathNumber2,
    mode='markers',
    name='Bathroom2',
    marker=Marker(
        color='rgb(255, 102, 0)',
        size=size2,
    )
)
data = Data([Bathroom1, Bathroom2])
layout = Layout(
    showlegend=True,
    title='Bubble Chart of Usage',
    xaxis=XAxis(title='Time'),
)
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig, filename='bubblechart')
