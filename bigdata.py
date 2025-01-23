import grpc, sys
import table_pb2_grpc, table_pb2

SERVER = "localhost:5440"
BATCH_COUNT = 400
BATCH_SIZE = 250_000

def main():
    if len(sys.argv) != 1:
        print("Usage: python3 bigdata.py")
        sys.exit(1)
    channel = grpc.insecure_channel(SERVER)
    stub = table_pb2_grpc.TableStub(channel)

    for batch in range(BATCH_COUNT):
        print(f"Batch {batch+1} of {BATCH_COUNT}: 0.25 million rows")
        rows = "x,y,z\n" + "\n".join([f"1,{i},{batch*1000+i%1000}" for i in range(BATCH_SIZE)])
        resp = stub.Upload(table_pb2.UploadReq(csv_data=bytes(rows, "utf-8")))

        if resp.error:
            print(resp.error)
            sys.exit(1)
        else:
            print("uploaded ")

if __name__ == "__main__":
    main()
