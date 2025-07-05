
# -*- coding: utf-8 -*-
import grpc
from concurrent import futures
import mysql.connector
import suscripciones_noticias_pb2 as pb2
import suscripciones_noticias_pb2_grpc as pb2_grpc
import time
import os
from cryptography.fernet import Fernet
import hashlib

class ServicioSuscripciones(pb2_grpc.SuscripcionesNoticiasServicer):
    def __init__(self, db):
        self.db = db
        self.fernet = Fernet(b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw=')
        
    def SubscribirCliente(self, request, context):
        cursor = self.db.cursor()
        try:
            # descifrar password
            password_plano = self.fernet.decrypt(request.password.encode()).decode()
            # calcular el md5
            password_md5 = hashlib.md5(password_plano.encode()).hexdigest()
            # verificar cliente
            cursor.execute(
                "SELECT id_cliente FROM clientes WHERE id_cliente=%s AND password_cliente=%s",
                (request.cliente_id, password_md5)
            )
            cliente = cursor.fetchone()
            if not cliente:
                return pb2.Respuesta(mensaje=f"El cliente {request.cliente_id} o contraseña incorrecta", exito=False)

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre=%s", (request.area,))
            area = cursor.fetchone()
            if not area:
                return pb2.Respuesta(mensaje=f"El área {request.area} no existe", exito=False)

            cursor.execute(
                "SELECT * FROM cliente_categoria WHERE id_cliente=%s AND id_categoria=%s",
                (request.cliente_id, area[0])
            )
            existe = cursor.fetchone()
            if existe:
                return pb2.Respuesta(mensaje=f"El cliente {request.cliente_id} ya estaba suscripto a {request.area}", exito=False)

            cursor.execute(
                "INSERT INTO cliente_categoria (id_cliente, id_categoria) VALUES (%s, %s)",
                (request.cliente_id, area[0])
            )
            self.db.commit()
            return pb2.Respuesta(mensaje=f"{request.cliente_id} se suscribió a {request.area}", exito=True)

        except Exception as e:
            print(f"Error en SubscribirCliente: {e}")
            return pb2.Respuesta(mensaje="Error al suscribir", exito=False)

    def BorrarSuscripcion(self, request, context):
        cursor = self.db.cursor()
        try:
            # desencriptar contraseña enviada
            password_plano = self.fernet.decrypt(request.password.encode()).decode()

            password_md5 = hashlib.md5(password_plano.encode()).hexdigest()

            # verificar cliente
            cursor.execute(
                "SELECT id_cliente FROM clientes WHERE id_cliente=%s AND password_cliente=%s",
                (request.cliente_id, password_md5)
            )
            cliente = cursor.fetchone()
            if not cliente:
                return pb2.Respuesta(mensaje="El cliente o contraseña incorrecta", exito=False)

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre=%s", (request.area,))
            area = cursor.fetchone()
            if not area:
                return pb2.Respuesta(mensaje=f"El área {request.area} no existe", exito=False)

            cursor.execute(
                "SELECT * FROM cliente_categoria WHERE id_cliente=%s AND id_categoria=%s",
                (request.cliente_id, area[0])
            )
            existe = cursor.fetchone()
            if not existe:
                return pb2.Respuesta(mensaje=f"El cliente {request.cliente_id} no estaba suscripto a {request.area}", exito=False)

            cursor.execute(
                "DELETE FROM cliente_categoria WHERE id_cliente=%s AND id_categoria=%s",
                (request.cliente_id, area[0])
            )
            self.db.commit()
            return pb2.Respuesta(mensaje=f"{request.cliente_id} se desuscribió de {request.area}", exito=True)

        except Exception as e:
            print(f"Error en BorrarSuscripcion: {e}")
            return pb2.Respuesta(mensaje="Error al borrar suscripción", exito=False)
            
    def ObtenerNoticiasDeArea(self, request, context):
        cursor = self.db.cursor()
        try:
            # desencriptar contraseña enviada
            password_plano = self.fernet.decrypt(request.password.encode()).decode()

            password_md5 = hashlib.md5(password_plano.encode()).hexdigest()

            cursor.execute(
                "SELECT id_cliente FROM clientes WHERE id_cliente=%s AND password_cliente=%s",
                (request.cliente_id, password_md5)
            )
            cliente = cursor.fetchone()
            if not cliente:
                return pb2.ListaNoticias(noticias=[])

            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre=%s", (request.area,))
            area = cursor.fetchone()
            if not area:
                return pb2.ListaNoticias(noticias=[])

            cursor.execute("""
                SELECT titulo, contenido, time_stamp
                FROM noticias
                JOIN noticia_categoria nc ON noticias.id_noticia = nc.id_noticia
                WHERE nc.id_categoria=%s
                ORDER BY time_stamp DESC
                LIMIT 3
            """, (area[0],))
            noticias = [
                pb2.Noticia(
                    titulo=row[0],
                    contenido=row[1],
                    fecha=str(row[2])
                ) for row in cursor.fetchall()
            ]
            return pb2.ListaNoticias(noticias=noticias)

        except Exception as e:
            print(f"Error en ObtenerNoticiasDeArea: {e}")
            return pb2.ListaNoticias(noticias=[])

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db = None
    for intento in range(10):
        try:
            db = mysql.connector.connect(
                host="mysql_db",
                user="root",
                password="root",
                database="consorcio"
            )
            print("ConexiÃ³n a la base de datos exitosa.")
            break
        except Exception as e:
            print(f"Intento {intento+1}/10: error conectando a MySQL: {e}")
            time.sleep(3)

    if not db:
        print("No se pudo conectar a MySQL despuÃ©s de 10 intentos.")
        return
    pb2_grpc.add_SuscripcionesNoticiasServicer_to_server(ServicioSuscripciones(db), server)   
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor escuchando en puerto 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
