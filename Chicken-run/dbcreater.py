import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()



#c.execute("CREATE TABLE accounts(username TEXT, password TEXT, level INTEGER)")
#c.execute("DROP TABLE accounts")
c.execute("UPDATE accounts SET level = (?)", (0,))
conn.commit()
