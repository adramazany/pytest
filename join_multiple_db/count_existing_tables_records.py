from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
def getCredential(self):
    return {'username': 'admin', 'password': 'fLAdmin_3Secure'}
auth_provider = PlainTextAuthProvider(username='admin', password='fLAdmin_3Secure')
node_ips = ['ls-dev-3']
cluster = Cluster(node_ips, auth_provider=auth_provider)
# session = cluster.connect('monitoring_stream')
session = cluster.connect()
#print(session.execute("SELECT * FROM monitoring_stream.monitoring_data_checkpoint").one())
# rows = session.execute('SELECT * FROM monitoring_stream.monitoring_data_checkpoint')
rows = session.execute("select * from system_schema.tables")
import pandas as pd
df = pd.DataFrame(rows._current_rows)
df = df[~df["keyspace_name"].str.startswith("system")]
# print(df.to_string())
tablesColumns = ['keyspace_name', 'table_name', 'count']
tablesDF = pd.DataFrame(columns=tablesColumns)
# tablesDF = pd.DataFrame(({
#     'keyspace_name':[],
#     'table_name':[],
#     'count':[]
# }))
print("=====================")
print("Cassandra all tables with count rows:")
print("---------------------")
for i,row in df.iterrows():
    # print(row)
    sql = f"select count(*) from {row['keyspace_name']}.{row['table_name']}"
    # print(sql)
    count = session.execute(sql).one()[0]
    # tablesDF.append({'keyspace_name':row['keyspace_name'],'table_name':row['table_name'],'count':count},ignore_index=True)
    # tablesDF.loc[i] = [row['keyspace_name'],row['table_name'],count] // Try using .loc[row_indexer,col_indexer] = value instead
    tablesDF = pd.concat([tablesDF, pd.DataFrame([[row['keyspace_name'],row['table_name'],count]], columns=tablesColumns ) ], ignore_index=True)
    tablesDF.index = tablesDF.index + 1
    # print(f"{row['keyspace_name']}.{row['table_name']}\t\t\t\t{count}")
print(tablesDF.count(),"\n", tablesDF.to_string())

print("=====================")
print("Cassandra all tables with count rows and NOT included in unconcernList:")
print("---------------------")
unconcernList = ['measurement_monitoring_stream.migrations','distinct_machine_value_stream.migrations','distinct_machine_message_stream.migrations','shift_performance_stream.current_shift_machine_run','application_monitoring_stream.migrations','monitoring_stream.current_machine_event','lot_performance_stream.current_lot_machine_run','distinct_recipe_stream.migrations']
emptyTablesDF = tablesDF[tablesDF['count']==0]
# emptyTablesDF['key'] = emptyTablesDF['keyspace_name']+'.'+emptyTablesDF['table_name'] # Try using .loc[row_indexer,col_indexer] = value instead
# emptyTablesDF.loc[:,'key'] = emptyTablesDF['keyspace_name']+'.'+emptyTablesDF['table_name']  # Try using .loc[row_indexer,col_indexer] = value instead
emptyTablesDF = emptyTablesDF.assign(key = lambda x: x['keyspace_name']+'.'+x['table_name'] )
emptyTablesDF = emptyTablesDF[~emptyTablesDF['key'].isin(unconcernList)]
pd.options.display.max_colwidth=250
print(emptyTablesDF.count(),"\n", emptyTablesDF['key'].to_string(index=False,length=0,))
print("=====================")
print("Cassandra empty tables included in prevEmptyList:")
print("---------------------")
# prevEmptyList = ['traceable_production_amount_stream.parent_item','unit_stream.parent_item','shift_performance_stream.partition_info','shift_performance_stream.shift_machine_run','traceable_production_measurement_stream.lot_material','traceable_production_measurement_stream.parent_item','equipment_value_stream.equipment_value','equipment_value_stream.partition_info','report_trigger_stream.manual_stopwatch','recipe_performance_stream.disconnected_state','material_map_distribution_stream.lot_material','material_map_distribution_stream.material_map_distribution','detailed_production_measurement_stats_stream.detailed_production_measurement_stats','audit_log_stream.current_parameter','error_stream.error','error_stream.partition_info','data_preparation_stream.item_meta_data','detailed_reject_amount_stream.detailed_reject_amount','machine_performance_stream.station_cycle_time']
prevEmptyList = ['traceable_production_measurement_stream.lot','traceable_production_measurement_stream.lot_material','traceable_production_measurement_stream.parent_item','traceable_production_measurement_stream.partition_info','traceable_production_measurement_stream.recipe','traceable_production_measurement_stream.traceable_production_measurement','report_trigger_stream.manual_stopwatch','audit_log_stream.current_parameter','data_preparation_stream.item_meta_data','data_preparation_stream.traceable_production_result_event']
# emptyTablesKeyDF = emptyTablesDF.set_index('key')
# print(emptyTablesKeyDF.to_string())
for p in prevEmptyList:
    row = emptyTablesDF[emptyTablesDF['key']==p]
    # if len(row)!=0:
    #     print(row['key'].iloc[0])
    if len(row)==0:
        print(p)
