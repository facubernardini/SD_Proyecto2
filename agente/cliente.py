import grpc
import agente_pb2
import agente_pb2_grpc
import readchar
import sys

def run():
    print("Bienvenido al servicio de noticias CONSORCIO DCIC: ")
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = agente_pb2_grpc.Servicio_AgenteStub(channel)
        id_cliente, password, login = realizar_login(stub)
        while login:               
            # Solicitud
            mostrar_menu()
            opcion = input("Elegí una opción (1-4): ").strip()
            opciones = {
                "1": lambda: obtener_noticias_24hs(stub, id_cliente, password),
                "2": lambda: suscribirse_nueva_categoria(stub, id_cliente, password),
            }
            if opcion == "4":
                print("Saliendo...")
                login = False
            elif opcion in opciones:
                opciones[opcion]()
            else:
                print("Opción inválida, por favor ingresá un número entre 1 y 4.")
        print("Muchas gracias por utilizar el servicio de noticias CONSORCIO DCIC")

def suscribirse_nueva_categoria(stub, id_cliente, password):
    area = input("Ingresá el area a la cual desea suscribirse: ").split()[0]
    request = agente_pb2.DatosSuscribirNuevaCategoria(cliente_id=id_cliente, area=area, password=password)
    response = stub.SuscribirNuevaCategoria(request)
    print("Respuesta del servidor:\n", response.mensaje)
    print("Resultado de la operacion: {response.exito} ")

def realizar_login(stub):
    from cryptography.fernet import Fernet

    clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='  # clave base64 en bytes
    cifrador = Fernet(clave)

    for intento in range(1, 4):  # hasta 3 intentos
        while True:
            entrada = input("Ingresá su número de documento: ").strip()
            if entrada.isdigit():
                id_cliente = int(entrada)  # <-- ahora es un entero real
                break
            else:
                print("Ingresá un número de documento válido.")
        password = leer_password_con_asteriscos()
        print(id_cliente)

        password_cifrada = cifrador.encrypt(password.encode())

        request = agente_pb2.LoginDatos(dni=id_cliente, password=password_cifrada)
        response = stub.Login(request)
        login_exitoso = response.resultado

        if login_exitoso:
            print("Login correcto\n\n")
            return id_cliente, password_cifrada, login_exitoso
        else:
            print(f"Login incorrecto (intento {intento}/3). Inténtelo nuevamente.\n")

    print("Demasiados intentos fallidos. Abortando.\n")
    return None, None, False

def obtener_noticias_24hs(stub, id_cliente, password):
    request = agente_pb2.noticiasRequest(nombre_usuario=id_cliente, password=password)
    response = stub.ObtenerNoticiasUltimas24hs(request)
    print("Respuesta del servidor:\n", response.mensaje)

def mostrar_menu():
    print("\n===== ¿Que servicio desea utilizar?=====")
    print("1. Obtener noticias últimas 24 hs")
    print("2. Suscribirse a una nueva categoria")
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
