import mysql.connector

conn = mysql.connector.connect(
         user='root',
         password='shreya00',
         host='localhost',
         database='trial')

mycursor = conn.cursor()

mycursor.execute({{que}})

conn.commit()

print(mycursor.rowcount, "implemented")

conn.close()