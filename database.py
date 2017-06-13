import psycopg2

def connectToDB(connectionConfig):
	conn = psycopg2.connect(connectionConfig)
	return conn

def disconnectFromDB(conn):
	conn.close()