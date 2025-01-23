import table_pb2_grpc, grpc
from table_pb2 import ColSumRes, UploadRes
from concurrent import futures
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from threading import Lock
import traceback

lock = Lock()
fileCount= 0
class TableServicer(table_pb2_grpc.TableServicer):
    
    def ColSum(self, request, context):
        global fileCount, lock
        #checks if theres any files (count)
        if fileCount== 0:
            return (ColSumRes(total= 0, error= ""))
         

        total_sum= 0
        #checks what format we should do
        error= ""
        try:
            if(request.format == "parquet"):
                for i in range(1, fileCount+1):

                    with lock:
                        parquet_path = os.path.join("storedParquet", "file_" + str(i))
                        table = pq.read_table(parquet_path)
                
                    # Converts the pandas table to pyArrow
                    if request.column in table.column_names:
                        column_data = table[request.column]
                        total_sum+= column_data.to_pandas().sum()
            
            else:
                for i in range(1, fileCount+1):
                    with lock:
                        csv_path = os.path.join("storedCSV", "file_" + str(i))
                        df = pd.read_csv(csv_path)

                    if request.column in df.columns:
                        total_sum+= df[request.column].sum()
        except Exception as e:
            error = traceback.format_exc()

        # print(total_sum)
        return (ColSumRes(total= total_sum, error= error))
    
    def Upload(self, request, context):
        global fileCount, lock

        error = ""

        with lock:
            fileCount+=1
            csv_path = os.path.join("storedCSV", "file_" + str(fileCount))
            parquet_path = os.path.join("storedParquet", "file_" + str(fileCount))

        try:
            with open(csv_path, "wb") as f:
                f.write(request.csv_data)
            

            #-------- parquet part
            df = pd.read_csv(csv_path)
            table = pa.Table.from_pandas(df)
            pq.write_table(table, parquet_path)

        except Exception as e:
            error = traceback.format_exc()

        return (UploadRes(error= error) )

print("start server")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=8), options=[("grpc.so_reuseport", 0)])
table_pb2_grpc.add_TableServicer_to_server(TableServicer(), server)                                                                                                                                                 
server.add_insecure_port("0.0.0.0:5440")
server.start()
server.wait_for_termination()