from os import environ

def initVariables(env, notification_type):
	email_url = ""
	path = ""
	connectionConfig = ""
	config = {}
	if notification_type == "forum":
		path = environ.get("FORUM_PATH")
	else:
		path = environ.get("SPAM_PATH")
	if env == "development":
		email_url = environ.get("STAGING_URL") + path
		connectionConfig = environ.get("STAGING_CONNECTION_STRING")
	else:
		email_url = environ.get("PRODUCTION_URL") + path
		connectionConfig = environ.get("PRODUCTION_CONNECTION_STRING")
	config['email_url'] = email_url
	config['connection'] = connectionConfig
	return config