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

CLAVE = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='

class LastNewsServicer(lastnews_pb2_grpc.LastNewsServicer):
    def InformLastNews(self, request, context):

        cifrador = Fernet(CLAVE)
        password = cifrador.decrypt(request.passw.encode())
        passwString = password.decode("utf-8")

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

        print("Solicitud de ultimas noticias realizada por usuario con id {}".format(request.client))
        noticias = ""
        nombreUsuario = ""
        if cnx and cnx.is_connected():

            with cnx.cursor() as cursor:

                cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}' AND password_cliente = MD5('{}');".format(request.client, passwString))
                for (nombre) in cursor:
                    nombreUsuario = nombre[0]

                if nombreUsuario=="":
                    print("El usuario con id {} es inválido.".format(request.client))
                    return lastnews_pb2.Response(news="Usuario invalido")
                else:
                    print("El usuario con id {} se llama {}.".format(request.client,nombreUsuario))

                cursor.execute("SELECT titulo, contenido FROM noticias as n JOIN noticia_categoria as nc JOIN (SELECT id_categoria FROM clientes as c JOIN cliente_categoria as b WHERE c.id_cliente = {} AND b.id_cliente = {} AND c.id_cliente = b.id_cliente ) as c WHERE n.id_noticia = nc.id_noticia AND nc.id_categoria = c.id_categoria;".format(request.client,request.client))

                for (titulo, contenido) in cursor:
                    noticias = noticias + "NOTICIA:{}: {}\n".format(titulo, contenido)

        cnx.close()
        print("Solicitud de {} Ejecutada correctamente".format(nombreUsuario))

        return lastnews_pb2.Response(news=noticias)

def iniciar_servidor():

    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lastnews_pb2_grpc.add_LastNewsServicer_to_server(
        LastNewsServicer(), servidor
    )
    print("Servidor gRPC escuchando en el puerto 50053...")
    servidor.add_insecure_port('[::]:50053')
    servidor.start()
    servidor.wait_for_termination()

if __name__ == '__main__':
    iniciar_servidor()