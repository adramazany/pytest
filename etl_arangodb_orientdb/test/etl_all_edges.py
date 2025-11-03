from pyArango.connection import *
import pyorient
from etl_arangodb_orientdb import ETL

src_conn = Connection(username="admin", password="admin")
src_db = src_conn["palamax_final"]


dest_client = pyorient.OrientDB("localhost", 2424)
dest_token = dest_client.get_session_token()
dest_client.set_session_token(dest_token)
dest_client.db_open( "palamax", "admin", "admin" )

# ETL(src_db, dest_client, "consistsOf").etl_edge_with_drop()
# ETL(src_db, dest_client, "identifies").etl_edge_with_drop()
# ETL(src_db, dest_client, "isLoadedFrom").etl_edge_with_drop()
# ETL(src_db, dest_client, "isUnloadedTo").etl_edge_with_drop()
# ETL(src_db, dest_client, "isParentOf").etl_edge_with_drop()
ETL(src_db, dest_client, "contains", "containsOf").etl_edge_with_drop()
# ETL(src_db, dest_client, "describes").etl_edge_with_drop()
# ETL(src_db, dest_client, "determines").etl_edge_with_drop()
# ETL(src_db, dest_client, "isUsedBy").etl_edge_with_drop()
# ETL(src_db, dest_client, "hasMeasurement").etl_edge_with_drop()
# ETL(src_db, dest_client, "hasTransfer").etl_edge_with_drop()

