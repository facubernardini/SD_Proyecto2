FROM python:3.11-slim

WORKDIR /app

COPY miembro.py .
COPY suscripciones_noticias.proto .

RUN pip install grpcio grpcio-tools mysql-connector-python cryptography

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. suscripciones_noticias.proto

CMD ["python", "miembro.py"]
