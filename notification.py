from os import environ
from os.path import join, dirname
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

email_credential = environ.get("EMAIL")
password_credential = environ.get("PASSWORD")

def createMessage(notification_type):
	content = {}
	if notification_type == "forum":
		content['subject'] = "No activity on Forum Post"
		content['body'] = "A forum post has been lacking in activity. Please review at "
	elif notification_type == "spam":
		content['subject'] = "Spam ALERT on the CORE Platform!"
		content['body'] = "We detected some Spam on the Forum. Please review at "
	return content

def send_email(subject, body, slug, email_url):
	fromaddr = email_credential
	toaddrs = ["calvingomez@ucsd.edu"]
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['Subject'] = subject
	 
	# body = "A forum post has been lacking in activity. Please review at " + email_url + slug
	msg.attach(MIMEText(body+email_url+slug, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email_credential, password_credential)
	text = msg.as_string()
	for toaddr in toaddrs:
		server.sendmail(fromaddr, toaddr, text)
	server.quit()