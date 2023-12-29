import sqlite3

conn=sqlite3.connect("contact_book.db")
c=conn.cursor()
c.execute("""CREATE TABLE contact(
          First_name text,
          Last_name text,
          Pho_no integer,
          Email text,
          Address text
        
)""")

conn.commit()
conn.close()