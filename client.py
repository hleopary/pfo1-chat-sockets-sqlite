import socket

# -----------------------------------------------------------------
# Configuración del cliente (debe coincidir con la del servidor)
# -----------------------------------------------------------------
HOST = "localhost"
PORT = 5000


def conectar_servidor() -> socket.socket:
    """
    Crea el socket del cliente y se conecta al servidor.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORT))
        print(f"[CLIENTE] Conectado al servidor {HOST}:{PORT}")
    except (ConnectionRefusedError, OSError) as error:
        print(f"[ERROR] No se pudo conectar a {HOST}:{PORT}. "
              f"¿Está el servidor corriendo? {error}")
        raise
    return cliente


if __name__ == "__main__":
    cliente = conectar_servidor()

    with cliente:
        while True:
            # El cliente envía mensajes hasta escribir "éxito"
            mensaje = input("Escribí tu mensaje (o 'éxito' para salir): ")
            if mensaje.lower() == "éxito":
                print("[CLIENTE] Terminando la conexión.")
                break

            cliente.sendall(mensaje.encode("utf-8"))

            # Muestra la respuesta del servidor para cada mensaje
            respuesta = cliente.recv(1024).decode("utf-8")
            print(f"[CLIENTE] Respuesta del servidor: {respuesta}")