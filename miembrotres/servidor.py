import grpc
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
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

# CLAVE = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='

class LastNewsServicer(lastnews_pb2_grpc.LastNewsServicer):
    def InformLastNews(self, request, context):

        # cifrador = Fernet(CLAVE)

        # password = cifrador.decrypt(request.passw.encode()) #asi se descencripta
        # print("request:",request)
        # print("password:",password)
        # passwString = password.decode("utf-8")
        # print("passwString:",passwString)

        try:
            cnx = connection.MySQLConnection(
                host="localhost",
                user="root",
                password="admin",
                database="consorcio"
                )
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        
        print("Solicitud de ultimas notificas realizada por usuario con id {}\n".format(request.client))
        noticias = ""
        nombreUsuario = ""
        if cnx and cnx.is_connected():

            with cnx.cursor() as cursor:

                # result = cursor.execute("SELECT nombre_categoria FROM vista_categorias_disponibles;")
                cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}';".format(request.client))
                for (nombre) in cursor:
                    nombreUsuario = nombreUsuario + "{}".format(nombre)
                
                print("El usuario con id {} se llama {}\n".format(request.client, nombreUsuario))

                # cursor.execute("SELECT titulo, contenido FROM vista_noticias_ultimas_24hs WHERE cliente = '{}';".format(nombreUsuario))

                # for (titulo, contenido) in cursor:
                #     noticias = noticias + "NOTICIA:{} {}\n".format(titulo, contenido)

        cnx.close()
        print("Solicitud de {} Ejecutada correctamente\n".format(nombreUsuario))
        return lastnews_pb2.Response(news=noticias)

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