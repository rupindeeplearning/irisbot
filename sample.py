import psycopg2

connection = psycopg2.connect(database="mlops", user="postgres", password="S4Eh3j35yktYImAjjSaZ", host="mlops-postgre.cqrst0aq2gxj.us-east-2.rds.amazonaws.com", port=5432)

cursor = connection.cursor()
cursor.execute("SELECT * from mlops.public.incidents1;")  
# Fetch all rows from database
record = cursor.fetchall()

print("Data from Database:- ", record)