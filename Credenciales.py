import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='prueba1'
    )