import mysql.connector

mydb = mysql.connector.connect (
    host = "localhost",
    user = "root",
    passwd = "",
    database = "zzz_db"
)

mycursor = mydb.cursor()