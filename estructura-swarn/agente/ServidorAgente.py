import grpc
import agente_pb2
import agente_pb2_grpc

import lastnews_pb2
import lastnews_pb2_grpc

import tareas_pb2
import tareas_pb2_grpc

import areas_pb2
import areas_pb2_grpc

from concurrent import futures

# Implementación del servicio Servicio_Agente
class ServicioAgenteServicer(agente_pb2_grpc.Servicio_AgenteServicer):
    def ObtenerNoticiasUltimas24hs(self, request, context):
        print(f"Solicitud de noticias delas ultimas 24hs recibida de usuario: {request.nombre_usuario}")
        with grpc.insecure_channel('lastnews:50053') as channel:    
            stubLastNews = lastnews_pb2_grpc.LastNewsStub(channel)
            requestLastNews = lastnews_pb2.ClientRequest(client=request.nombre_usuario,passw=request.password)
            responseLastNews = stubLastNews.InformLastNews(requestLastNews)
            return agente_pb2.noticiasInfo(mensaje=responseLastNews.news)
    
    def Login(self, request,context):
        print(f"Solicitud de Login recibida de usuario: {request.dni}")
        channel = grpc.insecure_channel('tareas:50055') 
        stub = tareas_pb2_grpc.TareasServiceStub(channel)
        response = stub.Login(tareas_pb2.LoginRequest(cliente=request.dni, password=request.password))
        #Aca debo conectarme al Login del miemro y devolver su respuesta
        return agente_pb2.ResultadoLogin(resultado=response.success)

    #def SuscribirNuevaCategoria(self, request, context):
        #print(f"Solicitud de suscripcion a nueva categoria del usuario {request.cliente_id} al area {request.area}")
        #Aca debo conectarme al Suscrbir nueva categoria del miembro
        #with grpc.insecure_channel('suscripciones:50054') as channel:    
            #stubSuscripciones = suscripciones_pb2_grpc.SuscripcionesNoticiasStub(channel)
            #requestSuscribirCliente =suscripciones_pb2.ClienteArea(cliente_id=request.nombre_usuario,area=request.area,password=request.password)
            #responseSuscribirNuevaCategoria = stubSuscripciones.SubscribirCliente(requestSuscribirCliente)
            #return agente_pb2.noticiasInfo(mensaje=responseSuscribirNuevaCategoria.mensaje)

    def AgregarCategoria(self, request, context):
        print(f"Se solicito la agregacion de una categoria por parte del usuario {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestAddArea = areas_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request.password,
                area=request.area
                )
            response = stub.AddArea(requestAddArea)
            return  agente_pb2.ResultadoAgregarCategoria(respuesta = response.response)

    def VerCategoriasInscripto(self, request, context):
        print(f"Se solicito ver categorias a las que esta inscripto por parte del usuarioÑ {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestShowAreas = areas_pb2.AreasRequest(
                client=request.cliente_id,
                passw=request.password
                )
            response = stub.ShowAreas(requestShowAreas)
            return  agente_pb2.RespuestaCategoriaInscripto(respuesta = response.response)
    
    def BorrarArea(self, request, context):
        print(f"Se solicito borrar la categoria {request.area} por parte del cliente {request.cliente_id}")
        with grpc.insecure_channel('adminareas:50054') as channel:
            stub = areas_pb2_grpc.AdminAreasStub(channel)
            requestDeleteArea = areas_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request.password,
                area = request.area
                )
            response = stub.DeleteArea(requestDeleteArea)
            return  agente_pb2.RespuestaCategoriaInscripto(respuesta = response.response)

    def BorrarSuscripcionCategoria(self, request, context):
        print(f"Se solicito la anulacion a una suscripcion a la categoria {request.area} del usuario {request.cliente_id} ")
        with grpc.insecure_channel('suscripciones:50054') as channel:    
            stubSuscripciones = suscripciones_pb2_grpc.SuscripcionesNoticiasStub(channel)
            requestSuscribirCliente =suscripciones_pb2.ClienteArea(cliente_id=request.nombre_usuario,area=request.area,password=request.password)
            responseSuscribirNuevaCategoria = stubSuscripciones.SubscribirCliente(requestSuscribirCliente)
            return agente_pb2.noticiasInfo(mensaje=responseSuscribirNuevaCategoria.mensaje)
    
    def ObtenerUltimasNoticias(self, request, context):
        print(f"Se solicitaron las ultimas noticias de la categoria {request.area} por parte del usuario {request.cliente_id}")
        with grpc.insecure_channel('lastnews:50053') as channel:
            stubLastNews = lastnews_pb2_grpc.LastNewsStub(channel)
        
            requestInformLastNews = lastnews_pb2.ClientRequest(
                client=request.cliente_id,
                passw=request.password
            )
            responseLastNews = stubLastNews.InformLastNews(requestInformLastNews)
        
            return agente_pb2.ResultadoSuscribirNuevaCategoria(mensaje=responseLastNews.news)
        return agente_pb2.ResultadoSuscribirNuevaCategoria(mensaje="\nNo se pudieron obtener las ultimas noticias - ERROR")

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agente_pb2_grpc.add_Servicio_AgenteServicer_to_server(ServicioAgenteServicer(), server)
    server.add_insecure_port('[::]:50052')  # Aquí definís el puerto del servidor agente
    server.start()
    print("Servidor Servicio_Agente escuchando en el puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    servir()
