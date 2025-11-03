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

src_consistsOf = src_db["consistsOf"]
print(src_consistsOf)

dest_client.command( "DROP CLASS consistsOf IF EXISTS UNSAFE" )
dest_client.command( "CREATE CLASS consistsOf extends E" )

count=0
for item in src_consistsOf.fetchAll():
    print(type(item), item.privates, item.getStore())
    store = item.getStore()
    fields=[]
    values=[]
    _from = store.pop("_from")
    _to = store.pop("_to")
    create_edge_cmd = f"create EDGE consistsOf FROM (select from PhysicalItem where _id='{_from}') TO (select from ItemPosition where _id='{_to}') CONTENT {str(store)}"
    print(create_edge_cmd)
    dest_client.command(create_edge_cmd)
    count+=1
    if count==100 : print(count)

