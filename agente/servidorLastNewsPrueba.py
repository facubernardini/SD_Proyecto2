from concurrent import futures
import grpc
import lastnews_pb2
import lastnews_pb2_grpc

# Implementación del servicio LastNews
class LastNewsServicer(lastnews_pb2_grpc.LastNewsServicer):
    def InformLastNews(self, request, context):
        print(f"Solicitud recibida de cliente: {request.client}")

        contenido = "Cristina presa!\n"

        return lastnews_pb2.Response(news=contenido)

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lastnews_pb2_grpc.add_LastNewsServicer_to_server(LastNewsServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor LastNews escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
