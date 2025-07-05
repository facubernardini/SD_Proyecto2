import grpc
from concurrent import futures
from cryptography.fernet import Fernet
import lastnews_pb2
import lastnews_pb2_grpc
import signal
import sys

def manejar_ctrl_c(signal, frame):
    print("Se ha presionado Ctrl+C. Finalizando el programa...")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_ctrl_c)

class LastNewsServicer(lastnews_pb2_grpc.LastNewsServicer):
    def InformLastNews(self, request, context):

        clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
        cifrador = Fernet(clave)

        password = cifrador.decrypt(request.passw.encode()) #asi se descencripta
        passwString = password.decode("utf-8")
        print("request:",request)
        print("password:",password)
        print("passwString:",passwString)
        return lastnews_pb2.Response(news="mensaje_respuesta")

def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    lastnews_pb2_grpc.add_LastNewsServicer_to_server(
        LastNewsServicer(), servidor
    )
    print("Servidor gRPC escuchando en el puerto 50051...")
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    servidor.wait_for_termination()

    

if __name__ == '__main__':
    iniciar_servidor()