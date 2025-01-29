import sqlite3

def create_connection():

    con = sqlite3.connect('owl-db.db')
    return con

def create_table(client):
    cur = client.cursor()

    try:
        cur.execute('''CREATE TABLE comp
               (id INTEGER PRIMARY KEY, entityA text, entityB text, isCompatible text,reason text, caveat text DEFAULT "None")''')
    except Exception as exp:
        print(exp)

def add_data(client, entityA, entityB,isCompatible,reason, caveat=None):
# Create table
        cur = client.cursor()


        if caveat is None:
            params = ( entityA, entityB,isCompatible,reason)
            cur.execute("INSERT INTO comp(entityA, entityB,isCompatible, reason) VALUES (?,?,?,?)",params)
        else:
            params = ( entityA, entityB,isCompatible,reason,caveat)
            cur.execute("INSERT INTO comp(entityA, entityB,isCompatible, reason,caveat) VALUES (?,?,?,?,?)",params)

        client.commit()

def get_output_all(client):
    cur = client.cursor()

    cur.execute('SELECT * FROM comp')
    rows = cur.fetchall()
    return rows


def query(client, licenA, licenB):
    cur = client.cursor()
    cur.execute("select reason, caveat from comp where (entityA=? and  entityB=?) and isCompatible='Yes'",(licenA,licenB))
    rows = cur.fetchall()
    return rows
    print(rows)

    
con = create_connection()
create_table(con)
get_output_all(con)

query(con,'LGPL-2.1','GPL-2.0')
# Add data portion
'''
handle = open('license.csv')
data = handle.readlines()

for line in data:
    item =  line.split(',')
    if len(item) == 4 :
        add_data(con, item[0],item[1],item[2],item[3])
    elif len(item) > 4:
        add_data(con, item[0],item[1],item[2],item[3], item[4])
    else:
        print("Odd:",item)
    #print(item)
    #print(len(item))
'''
#add_data(con, "eb","AS","Yes","blabhbl","adad")
#output = get_output_all(con)
#for out in output:
#    print(out)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#con.close()