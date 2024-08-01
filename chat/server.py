import socket
import threading
import struct

clientes = []  


def manejar_cliente(cliente_socket, direccion):
    try:
     
        cliente_socket.sendall(b"Por favor, introduce tu nombre de usuario: ")
        longitud_usuario = struct.unpack('>I', cliente_socket.recv(4))[0]
        nombre_usuario = cliente_socket.recv(longitud_usuario).decode('utf-8')
        print(f"{nombre_usuario} se ha conectado desde {direccion}")

        while True:
         
            longitud_mensaje_bytes = cliente_socket.recv(4)
            if not longitud_mensaje_bytes:
                print(f"{nombre_usuario} se ha desconectado.")
                break

            longitud_mensaje = struct.unpack('>I', longitud_mensaje_bytes)[0]
            mensaje = cliente_socket.recv(longitud_mensaje).decode('utf-8')
            mensaje_completo = f"{nombre_usuario}: {mensaje}"
            print(mensaje_completo)

         
            for cliente in clientes:
                if cliente != cliente_socket:
                    cliente.sendall(struct.pack('>I', len(mensaje_completo.encode('utf-8'))) + mensaje_completo.encode('utf-8'))
    except Exception as e:
        print(f"Error con {nombre_usuario}: {e}")
    finally:
        cliente_socket.close()
        clientes.remove(cliente_socket)


def servidor():
    host = '127.0.0.1'  
    puerto = 9999  

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(5)
    print(f"Servidor escuchando en {host}:{puerto}")

    while True:
        cliente_socket, direccion = servidor_socket.accept()
        clientes.append(cliente_socket)
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente_socket, direccion))
        hilo_cliente.start()

if __name__ == "__main__":
    servidor()  
