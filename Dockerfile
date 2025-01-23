FROM python:3.9-slim

WORKDIR /

COPY csvsum.py .
COPY parquetsum.py .
COPY simple.csv .
COPY table_pb2.py .
COPY upload.py .
COPY server.py .
COPY table.proto .
COPY table_pb2_grpc.py .
COPY storedCSV /storedCSV/
COPY storedParquet /storedParquet/


RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip install grpcio-tools==1.66.1 grpcio==1.66.1 protobuf==5.27.2 && \
    pip install pandas pyarrow
     
 

EXPOSE 5440

#our entry points
CMD ["python3", "-u", "/server.py"]