# -*- coding: utf-8 -*-
import grpc
from cryptography.fernet import Fernet
import sys
sys.path.append('/home/fedoras/noticias_consorcio/cliente')
import suscripciones_noticias_pb2 as pb2
import suscripciones_noticias_pb2_grpc as pb2_grpc

CLAVE_FERNET = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='
cifrador = Fernet(CLAVE_FERNET)

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.SuscripcionesNoticiasStub(channel)

    password_cifrado = cifrador.encrypt(b"1234").decode()

    resp1 = stub.SubscribirCliente(pb2.ClienteArea(
        cliente_id=1,
        area="Policial",
        password=password_cifrado
    ))
    print("SubscribirCliente:", resp1.mensaje)

    resp2 = stub.BorrarSuscripcion(pb2.ClienteArea(
        cliente_id=1,
        area="Policial",
        password=password_cifrado
    ))
    print("BorrarSuscripcion:", resp2.mensaje)

    lista = stub.ObtenerClientesPorArea(pb2.Area(nombre="Deportiva"))
    print("Clientes en Deportiva:", lista.clientes)

    noticias = stub.ObtenerNoticiasDeArea(pb2.ClienteArea(
        cliente_id=1,
        area="Deportiva",
        password=password_cifrado
    ))
    for n in noticias.noticias:
        print(f"[{n.fecha}] {n.titulo}: {n.contenido}")

if __name__ == "__main__":
    run()
