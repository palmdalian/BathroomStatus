#Import All the Libraries
import threading, re, time, os, sys
import sqlite3 as lite
from time import strftime
from BeautifulSoup import BeautifulSoup
import RPi.GPIO as GPIO

#Setup GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
GPIO.setup(23,GPIO.IN)

#Light pins
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

#Define some variables
count1 = 0
count2 = 0
pollTime = 1
statusPath = "/home/pi/status.html" 

#This makes sure that an HTML file exists..not completely necessary but helped while testing
os.remove("/home/pi/status.html")
with open("/home/pi/status.html", "w+") as f:
     				f.write("<html>\n<body>\n<div class='Bathroom2' style='background-color: #008000; font-size:xx-large;'>\nCalibrating, please wait...\n</div>\n<hr />\n<div class='Bathroom1' style='background-color: #FF0000; font-size:xx-large;'>\nCalibrating, please wait...\n</div>\n<hr />\n<br><div class='update'>Last updated: never</div>\n</head>\n</html>")
				f.close

def addToDatabase(timeOpened, count, bathNumber):
	#Connect to a SQLite Database I created
	con = lite.connect('bathroom.db')
	with con:
		cur = con.cursor()
		inputValues = (
			(timeOpened, count, bathNumber)
		)
		cur.executemany("INSERT INTO bath VALUES(NULL, ?, ?, ?)", (inputValues,))
		

def checkStatus():
    # call f() again in pollTime seconds
	threading.Timer(pollTime, checkStatus).start()
	global count1
	global count2
	if (GPIO.input(17)):
    	#Bathroom is closed
		updateHTML("Bathroom1", 1)
		count1 += pollTime
		GPIO.output(25, GPIO.LOW)
		
	else:
    	#Bathroom is open
		if (count1>0):
			addToDatabase(time.time(), count1, 1)
			updateHTML("Bathroom1", 0)
		count1 = 0
		GPIO.output(25, GPIO.HIGH)

		
	if (count1 >= 600):
		updateHTML("Bathroom1", 3)
		

	if (GPIO.input(23)):
    	#Bathroom is closed
		updateHTML("Bathroom2", 1) 
		GPIO.output(24, GPIO.LOW)
		count2 += pollTime
	else:
    	#Bathroom is open
		if (count2>0):
			#Write previous count to database when open
			addToDatabase(time.time(), count2, 2)
			updateHTML("Bathroom2", 0)
		count2 = 0
		GPIO.output(24, GPIO.HIGH)
	if (count2 >= 600):
		updateHTML("Bathroom2", 3)
	

def upload():
    # Uploading every 15 seconds
	threading.Timer(15, upload).start()
	os.system('/home/pi/Dropbox-Uploader/dropbox_uploader.sh -q upload /home/pi/status.html /Public/status.html')

def updateHTML(bathNumber, status):
	with open(statusPath, "r+") as f:
			data = f.read()
			if (status == 1):
				#Set status to closed with beautifulsoup
				replaceString = bathNumber + " is closed :("
				soup = BeautifulSoup(data)
				div = soup.find('div', {'class': bathNumber})
				div['style'] = 'background-color: #FF0000; font-size:xx-large;'
				div.string=replaceString
				#update last updated
				lastUpdated = soup.find('div', {'class': 'update'})
				lastUpdated.string="As of " + strftime("%H:%M:%S")
				f.close
				html = soup.prettify("utf-8")
				with open(statusPath, "wb") as file:
						file.write(html)
			if (status == 0):
				#Set status to open with beautifulsoup
				replaceString = bathNumber + " is open!"
				soup = BeautifulSoup(data)
				div = soup.find('div', {'class': bathNumber})
				div['style'] = 'background-color: #008000; font-size:xx-large;'
				div.string=replaceString
				#update last updated
				lastUpdated = soup.find('div', {'class': 'update'})
				lastUpdated.string="As of " + strftime("%H:%M:%S")
				f.close
				html = soup.prettify("utf-8")
				with open(statusPath, "wb") as file:
						file.write(html)
			if (status == 3):
				#If door has been closed too long
				replaceString = bathNumber + " has been closed for over 10 minutes. Might want to jiggle the handle."
				soup = BeautifulSoup(data)
				div = soup.find('div', {'class': bathNumber})
				div['style'] = 'background-color: #FFFF00; font-size:xx-large;'
				div.string=replaceString
				#update last updated
				lastUpdated = soup.find('div', {'class': 'update'})
				lastUpdated.string="As of " + strftime("%H:%M:%S")
				f.close
				html = soup.prettify("utf-8")
				with open(statusPath, "wb") as file:
						file.write(html)

#Set off inital functions so timers can kick in
checkStatus()
upload()
