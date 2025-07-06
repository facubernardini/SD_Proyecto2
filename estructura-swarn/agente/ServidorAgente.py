import grpc
import agente_pb2
import agente_pb2_grpc
from concurrent import futures

# Implementación del servicio Servicio_Agente
class ServicioAgenteServicer(agente_pb2_grpc.Servicio_AgenteServicer):
    def ObtenerNoticiasUltimas24hs(self, request, context):
        print(f"Solicitud de noticias delas ultimas 24hs recibida de usuario: {request.nombre_usuario}")
        #with grpc.insecure_channel('localhost:50051') as channel:    
        #    stubLastNews = lastnews_pb2_grpc.LastNewsStub(channel)
        #    requestLastNews = lastnews_pb2.ClientRequest(client=request.nombre_usuario,**{"pass": request.password})
        #    responseLastNews = stubLastNews.InformLastNews(requestLastNews)
        #    return agente_pb2.noticiasInfo(mensaje=responseLastNews.news)
        return agente_pb2.noticiasInfo(mensaje="Cristina presa!")
    
    def Login(self, request,context):
        print(f"Solicitud de Login recibida de usuario: {request.dni}")
        #Aca debo conectarme al Login del miemro y devolver su respuesta
        return agente_pb2.ResultadoLogin(resultado=True)

    def SuscribirNuevaCategoria(self, request, context):
        print(f"Solicitud de suscripcion a nueva categoria del usuario {request.cliente_id} al area {request.area}")
        #Aca debo conectarme al Suscrbir nueva categoria del miembro
        return agente_pb2.ResultadoSuscribirNuevaCategoria(mensaje="Su suscripcion ha sido aceptada", exito=True)
    
    def BorrarSuscripcionCategoria(self, request, context):
        print(f"Se solicito la anulacion a una suscripcion a la categoria {request.area} del usuario {request.cliente_id} ")
        #Aca debo conectarme a Borrar suscripcion del miembro
        return agente_pb2.ResultadoSuscribirNuevaCategoria(mensaje="se borro con exito", exito =True)
    
    def ObtenerUltimasNoticias(self, request, context):
        print(f"Se solicitaron las ultimas noticias de la categoria {request.area} por parte del usuario {request.cliente_id}")
        #Aca debo conectarme a obtener ultimas noticias del miembro
        return agente_pb2.ResultadoSuscribirNuevaCategoria(mensaje="Las ultimas noticias son:\nCristina Presa\nMilei clono a su hermana\n")

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agente_pb2_grpc.add_Servicio_AgenteServicer_to_server(ServicioAgenteServicer(), server)
    server.add_insecure_port('[::]:50052')  # Aquí definís el puerto del servidor agente
    server.start()
    print("Servidor Servicio_Agente escuchando en el puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
