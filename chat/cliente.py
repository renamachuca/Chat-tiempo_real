import socket
import threading
import struct
import sys


def enviar_mensajes(socket_cliente):
    try:
        while True:
            mensaje = input()  
            if mensaje.lower() == 'salir':  
                print("Saliendo del chat...")
                socket_cliente.close() 
                break  
            mensaje_codificado = mensaje.encode('utf-8')
            longitud_mensaje = struct.pack('>I', len(mensaje_codificado))
            socket_cliente.sendall(longitud_mensaje + mensaje_codificado)  
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
        socket_cliente.close()


def recibir_mensajes(socket_cliente):
    try:
        while True:
            # mensaje (4 bytes)
            longitud_mensaje_bytes = socket_cliente.recv(4)
            if not longitud_mensaje_bytes:
                print("Conexión cerrada por el servidor.")
                break
            longitud_mensaje = struct.unpack('>I', longitud_mensaje_bytes)[0]
            mensaje = socket_cliente.recv(longitud_mensaje).decode('utf-8')
            print(f"\r{mensaje}\n> ", end="")  # mensaje sin mostrar el id del usuario
            sys.stdout.flush()  # asegura inmediatamente
    except Exception as e:
        print(f"Error al recibir el mensaje: {e}")
        socket_cliente.close()


def cliente():
    host = '127.0.0.1'  
    puerto = 9999  

    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        socket_cliente.connect((host, puerto)) 

        print(f"Conectado al servidor {host}:{puerto}")

   
        nombre_usuario = input("Introduce tu nombre de usuario: ")
        nombre_usuario_codificado = nombre_usuario.encode('utf-8')
        longitud_nombre = struct.pack('>I', len(nombre_usuario_codificado))
        socket_cliente.sendall(longitud_nombre + nombre_usuario_codificado)


      
        hilo_envio = threading.Thread(target=enviar_mensajes, args=(socket_cliente,))
        hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(socket_cliente,))


        hilo_envio.start()
        hilo_recepcion.start()


        hilo_envio.join()
        hilo_recepcion.join()
    except Exception as e:
        print(f"Error al conectar con el servidor: {e}")
    finally:
        socket_cliente.close()

if __name__ == "__main__":
    cliente()  
