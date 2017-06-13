from os import environ
import notification
import config
import database
import psycopg2
import datetime

configVars = {}

def read_latest(conn):	
	cur = conn.cursor()
	cur.execute("SELECT id, subject, created_at, slug FROM forem_topics ORDER BY created_at DESC;")
	results = cur.fetchall()
	for i in range(0, len(results)):
		created_time = results[i][2]
		current_time = datetime.datetime.utcnow()
		diff = current_time - created_time

		if (diff.days==2):
			response_status = check_response(results[i][0])
			if response_status <=1:
				content = notification.createMessage("forum")
				notification.send_email(content['subject'],content['body'],results[i][3], configVars['email_url'])
				print("\nLack of activity at " + results[i][3] + ". Notification email sent!")

def check_response(post_id):
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM forem_posts WHERE topic_id=" + str(post_id) + ";")
	results=cur.fetchall()
	return results[0][0]

configVars = config.initVariables("development", "forum")
conn = database.connectToDB(configVars['connection'])
read_latest(conn)
database.disconnectFromDB(conn)