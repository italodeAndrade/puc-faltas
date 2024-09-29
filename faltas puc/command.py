import sqlite3
conn = sqlite3.connect('usuarios.db')            
cursor= conn.cursor()

cursor.execute("DELETE FROM usuarios")

conn.commit()
conn.close()