import grpc
import lastnews_pb2
import lastnews_pb2_grpc
from cryptography.fernet import Fernet

def ejecutar_cliente():
    # Crear un canal inseguro al servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        # Crear un stub (cliente)
        stub = lastnews_pb2_grpc.LastNewsStub(channel)

        # Crear una petición
        clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
        cifrador = Fernet(clave)
        password = "SoyPassword"
        password = cifrador.encrypt(password.encode())
        peticion = lastnews_pb2.ClientRequest(client=41460004,passw=password)

        # Realizar la llamada RPC
        try:
            respuesta = stub.InformLastNews(peticion)
            print(f"Respuesta del servidor: \n{respuesta.news}")
        except grpc.RpcError as e:
            print(f"Error en la llamada RPC: {e.code()}: {e.details()}")

if __name__ == '__main__':
    ejecutar_cliente()