import grpc
import agente_pb2
import agente_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = agente_pb2_grpc.Servicio_AgenteStub(channel)

        # Solicitud
        request = agente_pb2.noticiasRequest(nombre_usuario="claudio", password="1234")
        response = stub.ObtenerNoticiasUltimas24hs(request)

        print("Respuesta del servidor:\n", response.mensaje)

if __name__ == '__main__':
    run()
