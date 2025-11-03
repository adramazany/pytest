from pyArango.connection import *
import pyorient
from pyArango.query import SimpleQuery

from etl_arangodb_orientdb import ETL

src_conn = Connection(username="admin", password="admin")
src_db = src_conn["palamax_final"]


dest_client = pyorient.OrientDB("localhost", 2424)
dest_token = dest_client.get_session_token()
dest_client.set_session_token(dest_token)
dest_client.db_open( "palamax", "admin", "admin" )

src_lot = src_db["Lot"]
print(src_lot)

dest_client.command( "DROP CLASS Lot IF EXISTS UNSAFE" )
dest_client.command( "CREATE CLASS Lot extends V" )

count=0
for item in src_lot.fetchAll():
    print(type(item), item.privates, item.getStore())
    store = item.getStore()
    fields=[]
    values=[]
    for k in store:
        fields+=[k]
        values+=[ (f"'{store[k]}'") if isinstance(store[k], str) else str(store[k]) ]
    insert_cmd = f"insert into LOT ({','.join(fields)}) values({','.join(values)})"
    print(insert_cmd)
    dest_client.command(insert_cmd)
    count+=1
    if count==100 : print(count)

