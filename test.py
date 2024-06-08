import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

create_table_query = """
  CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
  )
"""

create_item_table = """
  CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    price FLOAT
  )
"""
cursor.execute(create_table_query)
cursor.execute(create_item_table)

user = ('jose', 'abcdef')

insert_user_query = """
  INSERT INTO user VALUES (NULL, ?, ?)
"""
# cursor.execute(insert_user_query, user)

users = [
  ('rolf', 'java-dkk'), ('malhone', 'rekkity-1')
]

# cursor.executemany(insert_user_query, users)

for row in cursor.execute("SELECT * FROM user"):
  print(row)

conn.commit()
conn.close()