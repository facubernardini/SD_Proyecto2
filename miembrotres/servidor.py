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
import threading
import time
import queue

BLUE = '\033[94m'
RESET = '\033[0m'
mensaje_queue = queue.Queue()
logger_sem = threading.Semaphore(1)

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
        
        # print("Solicitud de ultimas notificas realizada por usuario con id {}\n".format(request.client))
        mensaje_queue.put("Solicitud de ultimas notificas realizada por usuario con id {}".format(request.client))
        noticias = ""
        nombreUsuario = ""
        if cnx and cnx.is_connected():

            with cnx.cursor() as cursor:

                # result = cursor.execute("SELECT nombre_categoria FROM vista_categorias_disponibles;")
                cursor.execute("SELECT nombre FROM clientes WHERE id_cliente = '{}';".format(request.client))
                for (nombre) in cursor:
                    nombreUsuario = nombreUsuario + "{}".format(nombre)
                
                # print("El usuario con id {} se llama {}\n".format(request.client, nombreUsuario))
                mensaje_queue.put("El usuario con id {} se llama {}".format(request.client, nombreUsuario))

                # cursor.execute("SELECT titulo, contenido FROM vista_noticias_ultimas_24hs WHERE cliente = '{}';".format(nombreUsuario))

                # for (titulo, contenido) in cursor:
                #     noticias = noticias + "NOTICIA:{} {}\n".format(titulo, contenido)

        cnx.close()
        # print("Solicitud de {} Ejecutada correctamente\n".format(nombreUsuario))
        mensaje_queue.put("Solicitud de {} Ejecutada correctamente".format(nombreUsuario))

        return lastnews_pb2.Response(news=noticias)

def logger():
    while True:
        mensaje = mensaje_queue.get()
        if mensaje == "FIN":
            break
        logger_sem.acquire()
        print(f"{BLUE}{mensaje}{RESET}")
        logger_sem.release()

def show_categorias(cnx):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute("SELECT nombre_categoria FROM vista_categorias_disponibles;")
            for nombre_categoria in cursor:
                print(" - ",nombre_categoria[0])
    else:
        print("No se pudo ejecutar la operacion, se perdio la conexión a la base de datos")

def admin_categorias():
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
    print("Categorias disponibles:")
    show_categorias(cnx)

    try:
        opcion = input("1: Agregar categoria\n2: Eliminar categoria\n Cualquier caracter para salir\n")
    except KeyboardInterrupt:
        mensaje_queue.put("\nInterrupción del usuario")
        return
    except EOFError:
        mensaje_queue.put("\nFin de entrada detectado")
        return
    
    cnx.autocommit = True
    catName = ""
    if opcion=="1":
        catName = input("Ingrese el nombre de la nueva categoria: ")
        catName = catName.capitalize()
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                args = [catName]
                cursor.callproc("agregar_categoria", args)
                print("Categorias Modificadas")
                show_categorias(cnx)
        else:
            print("No se pudo ejecutar la operacion, se perdio la conexión a la base de datos")

    elif opcion=="2":
        catName = input("Ingrese el nombre de la categoria a eliminar: ")
        catName = catName.capitalize()
        if cnx and cnx.is_connected():
            with cnx.cursor() as cursor:
                args = [catName]
                cursor.callproc("eliminar_categoria", args)
                print("Categorias Modificadas")
                show_categorias(cnx)
        else:
            print("No se pudo ejecutar la operacion, se perdio la conexión a la base de datos")

    cnx.close

def service_dos():
    time.sleep(1)
    while True:
        try:
            opcion = input("Seleccione una opcion:\n 1:Administar categorias\n")
        except KeyboardInterrupt:
            mensaje_queue.put("\nInterrupción del usuario")
            return
        except EOFError:
            mensaje_queue.put("\nFin de entrada detectado")
            return
        
        logger_sem.acquire()
        print("selecciono la opcion:",opcion)
        if(opcion=="1"):
            admin_categorias()
        logger_sem.release()

def iniciar_servidor():

    hilo_logger = threading.Thread(target=logger, daemon=True)
    hilo_logger.start()
    
    hilo_admin = threading.Thread(target=service_dos, daemon=True)
    hilo_admin.start()

    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    lastnews_pb2_grpc.add_LastNewsServicer_to_server(
        LastNewsServicer(), servidor
    )
    # print("Servidor gRPC escuchando en el puerto 50051...")
    mensaje_queue.put("Servidor gRPC escuchando en el puerto 50051...")
    servidor.add_insecure_port('[::]:50051')
    servidor.start()
    servidor.wait_for_termination()

    mensaje_queue.put("FIN")
    hilo_logger.join()
    hilo_admin.join()

if __name__ == '__main__':
    iniciar_servidor()