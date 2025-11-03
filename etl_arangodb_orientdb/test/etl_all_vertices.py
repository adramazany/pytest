from pyArango.connection import *
import pyorient
from etl_arangodb_orientdb import ETL

src_conn = Connection(username="admin", password="admin")
src_db = src_conn["palamax_final"]


dest_client = pyorient.OrientDB("localhost", 2424)
dest_token = dest_client.get_session_token()
dest_client.set_session_token(dest_token)
dest_client.db_open( "palamax", "admin", "admin" )

ETL(src_db, dest_client, "Lot").etl_vertex_with_drop()
ETL(src_db, dest_client, "Recipe").etl_vertex_with_drop()
ETL(src_db, dest_client, "Operator").etl_vertex_with_drop()
ETL(src_db, dest_client, "MachineProductionDay").etl_vertex_with_drop()
ETL(src_db, dest_client, "ItemPosition").etl_vertex_with_drop()
ETL(src_db, dest_client, "PhysicalItem").etl_vertex_with_drop()
ETL(src_db, dest_client, "LogicalItem").etl_vertex_with_drop()
ETL(src_db, dest_client, "Item").etl_vertex_with_drop()
ETL(src_db, dest_client, "ItemMeasurement").etl_vertex_with_drop()
ETL(src_db, dest_client, "ItemTransfer").etl_vertex_with_drop()

