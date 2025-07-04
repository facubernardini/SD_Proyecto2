import grpc
from concurrent import futures
import lastnews_pb2
import lastnews_pb2_grpc

class LastNewsServicer(lastnews_pb2_grpc.LastNewsServicer):
    def RequestLastNews(self, request, context):
        print("request:",request)
        print("context:",context)
        return lastnews_pb2.Response(news="mensaje_respuesta")

def iniciar_servidor():
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lastnews_pb2_grpc.add_LastNewsServicer_to_server(
        LastNewsServicer(), servidor
    )
    print("Servidor gRPC escuchando en el puerto 50051...")
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()