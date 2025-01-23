import grpc, sys, time
import table_pb2_grpc, table_pb2

SERVER = "localhost:5440"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 csvsum.py <COLUMN>")
        sys.exit(1)
    column = sys.argv[1]
    channel = grpc.insecure_channel(SERVER)
    stub = table_pb2_grpc.TableStub(channel)
    start = time.time()
    resp = stub.ColSum(table_pb2.ColSumReq(column=column, format="csv"))
    end = time.time()
    print(f"{round((end-start)*1000, 1)} ms")

    if resp.error:
        print(resp.error)
    else:
        print(resp.total)

if __name__ == "__main__":
    main()
