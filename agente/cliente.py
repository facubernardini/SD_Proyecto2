import grpc
import agente_pb2
import agente_pb2_grpc
import readchar
import sys

def run():
    print("Bienvenido al servicio de noticias CONSORCIO DCIC: ")
    with grpc.insecure_channel('192.168.239.132:50052') as channel:
        stub = agente_pb2_grpc.Servicio_AgenteStub(channel)
        id_cliente, password, login = realizar_login(stub)
        while login:               
            # Solicitud
            mostrar_menu()
            opcion = input("Elegí una opción (1-4): ").strip()
            opciones = {
                "1": lambda: obtener_noticias_24hs(stub, id_cliente, password),
                "2": lambda: suscribirse_nueva_categoria(stub, id_cliente, password),
                "3": lambda: agregar_nueva_categoria(stub, id_cliente, password),
                "4": lambda: obtener_ultimas_noticias_categoria( stub, id_cliente, password),
                "5": lambda: ver_categorias_inscripto(stub, id_cliente, password),
                "6": lambda: borrar_area(stub, id_cliente, password),
                "7": lambda: agregar_noticia(stub, id_cliente, password),
            }
            if opcion == "8":
                print("Saliendo...")
                login = False
            elif opcion in opciones:
                opciones[opcion]()
            else:
                print("Opción inválida, por favor ingresá un número entre 1 y 6.")
        print("Muchas gracias por utilizar el servicio de noticias CONSORCIO DCIC")

def agregar_noticia(stub, id_cliente, password):
    titulo = input("Ingrese el titulo de la noticia:")
    contenido = input("Ingrese el contenido de la noticia: ")
    area = input("Ingrese el area a la cual pertenece la noticia: ")
    request = agente_pb2.DatosEnviarNoticia(cliente_id=id_cliente, password=password, titulo=titulo, contenido=contenido,area=area)
    responde = stub.EnviarNoticia(request)
    print(f"Respuesta del servidor: {responde.respuesta}")

def borrar_area(stub, id_cliente, password):
    area = input("Ingrese el nombre del area que desea eliminar: ").split()[0]
    request = agente_pb2.DatosBorrarArea(cliente_id=id_cliente ,password=password, area = area)
    response = stub.BorrarArea(request)
    print(f"Respuesta del servidor: ")


def ver_categorias_inscripto(stub, id_cliente, password):
    request = agente_pb2.DatosVerCategoriasInscripto(cliente_id=id_cliente ,password=password)
    response = stub.BorrarArea(request)
    print(f"Respuesta del servidor: {response.respuesta}")

def agregar_nueva_categoria(stub, id_cliente , password):
    area = input("Ingrese el nombre de la categoria: ").split()[0]
    request = agente_pb2.DatosAgregarCategoria(cliente_id=id_cliente ,password=password,area=area)
    response = stub.AgregarCategoria(request)
    print(f"Respuesta del servidor: {response.respuesta}")

def obtener_ultimas_noticias_categoria(stub, id_cliente, password):
    #area = input("Ingrese el nombre de la categoria de la cual desea obtener las ultimas noticias: ").split()[0]
    area = ""
    request = agente_pb2.DatosObtenerUltimasNoticias(cliente_id=id_cliente ,password=password,area=area)
    response = stub.ObtenerUltimasNoticias(request)
    print(f"Las ultimas noticias del area {area} son: \n {response.mensaje}")

def borrarse_de_una_suscripcion(stub, id_cliente, password):
    area = input("Ingrese el nombre de la categoria de la cual desea anular su suscripcion: ").split()[0]
    request = agente_pb2.DatosSuscribirNuevaCategoria(cliente_id=id_cliente, area=area, password=password)
    response = stub.BorrarSuscripcionCategoria(request)
    print("Respuesta del servidor:\n", response.mensaje)
    print(f"Resultado de la operacion: {response.exito} ")

def suscribirse_nueva_categoria(stub, id_cliente, password):
    area = input("Ingresá el area a la cual desea suscribirse: ").split()[0]
    request = agente_pb2.DatosSuscribirNuevaCategoria(cliente_id=id_cliente, area=area, password=password)
    response = stub.SuscribirNuevaCategoria(request)
    print("Respuesta del servidor:\n", response.mensaje)
    print("Servicio en mantenimiento")

def realizar_login(stub):
    from cryptography.fernet import Fernet

    clave = b'J8vKqAnGsyiQUKmM2hRsaM4TQEL8gtjCKxgMrzG2Fnw='  # clave base64 en bytes
    cifrador = Fernet(clave)

    for intento in range(1, 4):  # hasta 3 intentos
        while True:
            entrada = input("Ingresá su número de documento: ").strip()
            if entrada.isdigit():
                id_cliente = int(entrada)  #Lo transoformo a entero
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
    print(f"Respuesta del servidor:\n {response.mensaje}")

def mostrar_menu():
    print("\n===== ¿Que servicio desea utilizar?=====")
    print("1. Obtener noticias últimas 24 hs")
    print("2. Suscribirse a una nueva categoria")
    print("3. Agregar Nueva Categoria")
    print("4. Obtener ultimas noticias")
    print("5. Ver categorias inscripto")
    print("6. Borrar area")
    print("7. Agregar noticia")
    print("8. Salir")
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
