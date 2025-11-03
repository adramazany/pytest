import pyorient


client = pyorient.OrientDB("localhost", 2424)
token = client.get_session_token()
client.set_session_token(token)
# session_id = client.connect( "admin", "admin" )
client.db_open( "palamax", "admin", "admin" )

# //create class
# cluster_id = client.command( "create class my_class extends V" )

# //create property
# cluster_id = client.command( "create property my_class.id Integer" )
# cluster_id = client.command( "create property my_class.name String" )

# //insert record
client.command("insert into my_class (id,name) values( 1202, 'satish2')")

# cluster_id = client.command( "create class Lot extends V" )
# client.command("insert into Lot ('id','key','machineId', 'startTimestamp', 'endTimestamp', 'lotName', 'lotId' ) "
#                "values( 'Lot/f3cac3c1e4a0d93db1e0d573e000ca61', 'f3cac3c1e4a0d93db1e0d573e000ca61', 'Stacker123',1695214828526,1695214848666,'Cell Production Bach #1695214828512','11bec92c-443f-4a66-a6a9-b930e8e295fd')")
