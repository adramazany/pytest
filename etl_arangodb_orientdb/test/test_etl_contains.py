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

src_containsOf = src_db["contains"]
print(src_containsOf)

dest_client.command( "DROP CLASS containsOf IF EXISTS UNSAFE" )
dest_client.command( "CREATE CLASS containsOf extends E" )

count=0
for item in src_containsOf.fetchAll():
    print(type(item), item.privates, item.getStore())
    store = item.getStore()
    fields=[]
    values=[]
    _from = store.pop("_from")
    _to = store.pop("_to")
    create_edge_cmd = f"create EDGE containsOf FROM (select from Lot where _id='{str(_from)}') TO (select from Item where _id='{str(_to)}') "
    print(create_edge_cmd)
    try:
        dest_client.command(create_edge_cmd)
    except pyorient.exceptions.PyOrientCommandException as ex:
        # RETRY another time in case of this error
        print("One of vertices of _from or _to are not exists:", ex, create_edge_cmd)
    count+=1
    if count==100 : print(count)

