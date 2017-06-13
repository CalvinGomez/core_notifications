import requests
import json
import psycopg2
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

conn = ""

def read_latest():
	global conn
	conn = psycopg2.connect("dbname=ebdb user=thecore  host='aa628jq1wf07wp.ctkyddfipr6g.us-west-2.rds.amazonaws.com' password='thisTown!'")
	
	cur = conn.cursor()
	cur.execute("SELECT text, created_at FROM forem_posts ORDER BY created_at DESC;")
	results = cur.fetchall()
	spam_flag = 0
	for i in range(0, len(results)):
		created_time = results[i][1]
		current_time = datetime.datetime.utcnow()
		diff = current_time - created_time
		if (diff.seconds<=60 and diff.days==0):
			spam_flag = 1
			spam_status = check_spam(results[i][0])
			if spam_status=="SPAM":
				print(str(i) + ": " + spam_status)
				send_email()
			else:
				print(str(i) + ": " + "OK")
		else:
			break
	if spam_flag == 0:
		print("No Spam Posts in the last one minute.")
	conn.close()

def send_email():
	fromaddr = "thecore@eng.ucsd.edu"
	toaddrs = ["calvingomez@ucsd.edu"]
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['Subject'] = "Spam ALERT on the CORE Platform!"
	 
	body = "We detected some Spam on the Forum. Please review at https://thecore-platform.ucsd.edu/forums/questions-answers"
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("thecore@eng.ucsd.edu", "ConnectedandOpenResearchEthics")
	text = msg.as_string()
	for toaddr in toaddrs:
		server.sendmail(fromaddr, toaddr, text)
	server.quit()
	

def check_spam(comment):
	data = json.dumps({
		"comment": comment,
		"ip"     : "173.245.66.156",
		"site"   : "http://core-stage.us-west-2.elasticbeanstalk.com"
	})
	resp = requests.post(url="http://test.blogspam.net:9999/", data=data)
	return json.loads(resp.content.decode('utf-8'))['result']

read_latest()
# print(check_spam("Hi"))