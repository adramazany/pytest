import threading
import time

import pyorient


class ETL:

    def __init__(self, src_db, dest_client: pyorient.OrientDB, col_name, dest_col_name=None):
        self.src_db         = src_db
        self.dest_client    = dest_client
        self.src_col_name   = col_name
        self.dest_col_name  = dest_col_name if dest_col_name else col_name


    def etl_vertex_with_drop(self):
        self.dest_client.command(f"DROP CLASS {self.dest_col_name} IF EXISTS UNSAFE")
        self.dest_client.command(f"CREATE CLASS {self.dest_col_name} EXTENDS V")
        self.dest_client.command(f"CREATE PROPERTY {self.dest_col_name}._id STRING (MANDATORY TRUE)" )

        self.etl_vertex_append()

    def etl_vertex_append(self):
        start_ts = time.time()
        print(f"etl_vertex_append start for {self.dest_col_name}.")
        src_lot = self.src_db[self.src_col_name]
        # print(src_lot)
        count = 0
        for item in src_lot.fetchAll():
            # print(type(item), item.privates, item.getStore())
            store = item.getStore()
            fields = []
            values = []
            for k in store:
                fields += [k]
                # values += [(f"'{store[k]}'") if isinstance(store[k], str) else str(store[k])]
                values += [(f"'{store[k]}'") if isinstance(store[k], str) else ("'{}'".format(str(store[k]).replace("'","\\'"))) if  isinstance(store[k], list) else str(store[k])]
                # values += [(f"'{store[k]}'") if not isinstance(store[k], (int, float, complex)) else str(store[k])]
            insert_cmd = f"insert into {self.dest_col_name} ({','.join(fields)}) values({','.join(values)})"
            # print(insert_cmd)
            self.dest_client.batch()
            self.dest_client.command(insert_cmd)
            count += 1
            if count%1000 == 0: print(count)
        self.dest_client.command(f"CREATE INDEX {self.dest_col_name}.pk on {self.dest_col_name}(_id) UNIQUE_HASH_INDEX")
        print(f"inserting {count} record in {self.dest_col_name} done at [{time.time()-start_ts}]s.")

    def etl_vertex_append_batch(self):
        start_ts = time.time()
        print(f"etl_vertex_append start for {self.dest_col_name}.")
        src_lot = self.src_db[self.src_col_name]
        # print(src_lot)
        count = 0
        for item in src_lot.fetchAll():
            # print(type(item), item.privates, item.getStore())
            store = item.getStore()
            fields = []
            values = []
            for k in store:
                fields += [k]
                # values += [(f"'{store[k]}'") if isinstance(store[k], str) else str(store[k])]
                values += [(f"'{store[k]}'") if isinstance(store[k], str) else ("'{}'".format(str(store[k]).replace("'","\\'"))) if  isinstance(store[k], list) else str(store[k])]
                # values += [(f"'{store[k]}'") if not isinstance(store[k], (int, float, complex)) else str(store[k])]
            insert_cmd = f"insert into {self.dest_col_name} ({','.join(fields)}) values({','.join(values)})"
            # print(insert_cmd)
            self.dest_client.batch()
            self.dest_client.command(insert_cmd)
            count += 1
            if count%1000 == 0: print(count)
        self.dest_client.command(f"CREATE INDEX {self.dest_col_name}.pk on {self.dest_col_name}(_id) UNIQUE_HASH_INDEX")
        print(f"inserting {count} record in {self.dest_col_name} done at [{time.time()-start_ts}]s.")

    def etl_edge_with_drop(self):
        self.dest_client.command(f"DROP CLASS {self.dest_col_name} IF EXISTS UNSAFE")
        self.dest_client.command(f"CREATE CLASS {self.dest_col_name} EXTENDS E")
        self.dest_client.command(f"CREATE PROPERTY {self.dest_col_name}._id STRING (MANDATORY TRUE)" )

        self.etl_edge_append()

    def etl_edge_append(self):
        start_ts = time.time()
        print(f"etl_edge_append start for {self.dest_col_name}.")
        src_lot = self.src_db[self.src_col_name]
        # print(src_lot)
        count = 0
        for item in src_lot.fetchAll():
            # print(type(item), item.privates, item.getStore())
            store = item.getStore()
            fields = []
            values = []
            _from = store.pop("_from")
            _to = store.pop("_to")
            create_edge_cmd = f"CREATE EDGE {self.dest_col_name} FROM (SELECT FROM {_from.split('/')[0]} WHERE _id='{_from}') TO (SELECT FROM {_to.split('/')[0]} WHERE _id='{_to}') CONTENT {str(store)}"
            # print(create_edge_cmd)
            try:
                self.dest_client.command(create_edge_cmd)
                count += 1
            except pyorient.exceptions.PyOrientCommandException as ex:
                print("One of vertices of _from or _to are not exists:",ex,create_edge_cmd)
            except TimeoutError as ex:
                print("TimeoutError:",ex,create_edge_cmd)

            if count%1000 == 0: print(count)
        print(f"creating {count} edge in {self.dest_col_name} done at [{time.time()-start_ts}]s.")

