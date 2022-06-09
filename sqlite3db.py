import sqlite3
from databaseClass import Interface

# file location for the connection
conn = sqlite3.connect('interfaces.db')
# the cursor to point the database connection
c = conn.cursor()
#creating the table it should be quried only once or the table from the db file
# c.execute("""CREATE TABLE interfaces (
#             ifName text,
#             ifInoctets integer,
#             ifOutoctets integer,
#             speed integer
#             )""")

#
# c.execute("""CREATE TABLE lo (
#             ifInoctets integer,
#             ifOutoctets integer,
#             speed integer
#             )""")

# c.execute("""CREATE TABLE eth (
#             ifInoctets integer,
#             ifOutoctets integer,
#             speed integer
#             )""")

# c.execute("""CREATE TABLE wlan (
#             ifInoctets integer,
#             ifOutoctets integer,
#             speed integer
#             )""")



# insert new values to the table
# def insert_interface(interface):
#     with conn:
#         c.execute("INSERT INTO interfaces VALUES (:ifname, :ifInoctets, :ifOutoctets, :speed)", {'ifname': interface.ifName , 'ifInoctets': interface.ifInoctets, 'ifOutoctets': interface.ifOutoctets, 'speed': interface.speed})

#insterting into the ifinoctets
def insert_ifInOctets(ifinoctets) :
    with conn:
        c.execute("INSERT INTO interfaces (ifInOctets) VALUES ( :ifInoctets)", {'ifInoctets' : ifinoctets })
#inserting into the ifoutoctets
def insert_ifOutOctets(ifoutoctets) :
    with conn:
        c.execute("INSERT INTO interfaces (ifOutOctets) VALUES ( :ifoutoctets)", {'ifoutoctets' : ifoutoctets })
        
# get the value of an interface by its name
# def get_interface_by_name(ifName):
#     c.execute("SELECT * FROM interfaces WHERE ifName=:ifName", {'ifName': ifName})
#     return c.fetchall()

# get the value of an interface by its speed
def get_interface_by_speed(speed):
    c.execute("SELECT * FROM interfaces WHERE speed=:speed", {'speed': speed})
    return c.fetchall()

# to update the octets values for an interface 
# def update_octets(interface, speed):
    # with conn:
    #     c.execute("""UPDATE interfaces SET speed = :speed
    #                 WHERE ifInoctets = :ifInoctets AND ifOutoctets = :ifOutoctets""",
    #               {'ifInoctets': interface.ifInoctets, 'ifOutoctets': interface.ifOutoctets, 'speed': speed})

# to remove an interface from the table
# def remove_interface(interface):
#     with conn:
#         c.execute("DELETE from interfaces WHERE ifInoctets = :ifInoctets AND ifOutoctets = :ifOutoctets",
#                   {'ifInoctets': interface.ifInoctets, 'ifOutoctets': interface.ifOutoctets})

# interface1 = Interface('ifname.1' , 100000, 235050, 2133)
# interface2 = Interface('ifname.2' , 100000, 235050, 2133)
# insert_interface(interface1)
# insert_interface(interface2)



# print(get_interface_by_name('ifname.1'))

#insert into a table data of the interfaces
def insertDataForLo( inoctet, outoctet, speed):
    with conn:
        c.execute("INSERT INTO lo VALUES (:ifInoctets, :ifOutoctets, :speed)", \
            {'ifInoctets': inoctet, 'ifOutoctets': outoctet, 'speed': speed})

def insertDataForEth( inoctet, outoctet, speed):
    with conn:
        c.execute("INSERT INTO eth VALUES (:ifInoctets, :ifOutoctets, :speed)", {'ifInoctets': inoctet, 'ifOutoctets': outoctet, 'speed': speed})
        
def insertDataForWlan( inoctet, outoctet, speed):
    with conn:
        c.execute("INSERT INTO wlan VALUES (:ifInoctets, :ifOutoctets, :speed)", {'ifInoctets': inoctet, 'ifOutoctets': outoctet, 'speed': speed})        


conn.commit()
