from cryptography.fernet import Fernet
import grpc
import agente_pb2
import agente_pb2_grpc
import readchar
import sys

def run():
    clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='  # cadena base64 en bytes
    cifrador = Fernet(clave)
    print("Bienvenido al servicio de noticias CONSORCIO DCIC: ")
    id_cliente = input("Ingresá su numero de documento: ")
    password = leer_password_con_asteriscos()
    print(id_cliente)
    password = cifrador.encrypt(password.encode())

    #ACA DEBERIA HACER EL LOGIN
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = agente_pb2_grpc.Servicio_AgenteStub(channel)
        request = agente_pb2.LoginDatos(dni=id_cliente, password=password)
        response = stub.Login(request)
        login =response.resultado
        if login == True:
            print("Login correcto\n\n")
        else:
            print("Login incorrecto.\nIntentelo nuevamente\n")
        while login:               
            # Solicitud
            mostrar_menu()
            opcion = input("Elegí una opción (1-4): ").strip()
            opciones = {
                "1": lambda: obtener_noticias_24hs(stub, id_cliente, password),
            }
            if opcion == "4":
                print("Saliendo...")
                login = False
            elif opcion in opciones:
                opciones[opcion]()
            else:
                print("Opción inválida, por favor ingresá un número entre 1 y 4.")
        print("Muchas gracias por utilizar el servicio de noticias CONSORCIO DCIC")

def obtener_noticias_24hs(stub, id_cliente, password):
    request = agente_pb2.noticiasRequest(nombre_usuario=id_cliente, password=password)
    response = stub.ObtenerNoticiasUltimas24hs(request)
    print("Respuesta del servidor:\n", response.mensaje)

def mostrar_menu():
    print("\n===== ¿Que servicio desea utilizar?=====")
    print("1. Obtener noticias últimas 24 hs")
    print("2. Consultar estado del agente")
    print("3. Enviar reporte")
    print("4. Salir")
    print("===============================")

def leer_password_con_asteriscos():
    print("Ingresá tu contraseña: ", end='', flush=True)
    password = ""
    while True:
        char = readchar.readchar()
        if char in ('\r', '\n'):
            print('')
            break
        elif char == '\x03':  # Ctrl+C
            print("\nCancelado.")
            sys.exit(0)
        elif char == '\x7f':  # Backspace
            if password:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            password += char
            sys.stdout.write('*')
            sys.stdout.flush()
    return password


if __name__ == '__main__':
    run()
