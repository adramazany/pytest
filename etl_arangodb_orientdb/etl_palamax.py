from pyArango.connection import *
import pyorient
from etl_arangodb_orientdb import ETL

############### local final_palax
# src_conn = Connection(arangoURL='http://127.0.0.1:8529', username="admin", password="admin")
# src_db = src_conn["palamax_final"]
# dest_client = pyorient.OrientDB("localhost", 2424)
# dest_token = dest_client.get_session_token()
# dest_client.set_session_token(dest_token)
# dest_client.db_open( "palamax_final", "admin", "admin" )

############### ls-dev-5 final_palax
src_conn = Connection(arangoURL='http://ls-dev-5:8529', username="admin", password="test")
src_db = src_conn["palamax"]

dest_client = pyorient.OrientDB("localhost", 2424)
dest_token = dest_client.get_session_token()
dest_client.set_session_token(dest_token)
dest_client.db_open( "palamax", "admin", "admin" )

############### ETL vertices
# ETL(src_db, dest_client, "Lot").etl_vertex_with_drop()
# ETL(src_db, dest_client, "Recipe").etl_vertex_with_drop()
# ETL(src_db, dest_client, "Operator").etl_vertex_with_drop()
# ETL(src_db, dest_client, "MachineProductionDay").etl_vertex_with_drop()
# ETL(src_db, dest_client, "ItemPosition").etl_vertex_with_drop()
# ETL(src_db, dest_client, "PhysicalItem").etl_vertex_with_drop()
# ETL(src_db, dest_client, "LogicalItem").etl_vertex_with_drop()
# ETL(src_db, dest_client, "Item").etl_vertex_with_drop()
ETL(src_db, dest_client, "ItemMeasurement").etl_vertex_with_drop()
ETL(src_db, dest_client, "ItemTransfer").etl_vertex_with_drop()

############### ETL edges
ETL(src_db, dest_client, "consistsOf").etl_edge_with_drop()
ETL(src_db, dest_client, "identifies").etl_edge_with_drop()
ETL(src_db, dest_client, "isLoadedFrom").etl_edge_with_drop()
ETL(src_db, dest_client, "isUnloadedTo").etl_edge_with_drop()
ETL(src_db, dest_client, "isParentOf").etl_edge_with_drop()
ETL(src_db, dest_client, "contains", "containsOf").etl_edge_with_drop()
ETL(src_db, dest_client, "describes").etl_edge_with_drop()
ETL(src_db, dest_client, "determines").etl_edge_with_drop()
ETL(src_db, dest_client, "isUsedBy").etl_edge_with_drop()
ETL(src_db, dest_client, "hasMeasurement").etl_edge_with_drop()
ETL(src_db, dest_client, "hasTransfer").etl_edge_with_drop()

