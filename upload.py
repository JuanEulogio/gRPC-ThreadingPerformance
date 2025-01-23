import grpc, sys
import table_pb2_grpc, table_pb2

SERVER = "localhost:5440"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 upload.py <CSV_PATH>")
        sys.exit(1)
    path = sys.argv[1]
    channel = grpc.insecure_channel(SERVER)
    stub = table_pb2_grpc.TableStub(channel)
    with open(path, "rb") as f:
        data = f.read() # binary "bytes" data
    resp = stub.Upload(table_pb2.UploadReq(csv_data=data))

    if resp.error:
        print(resp.error)
    else:
        print("success")

if __name__ == "__main__":
    main()
