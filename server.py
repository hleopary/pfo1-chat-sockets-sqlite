import socket
import sqlite3
from datetime import datetime

# -----------------------------------------------------------------
# Configuración del servidor
# -----------------------------------------------------------------
HOST = "localhost"          # Escucha en la máquina local
PORT = 5000                 # Puerto indicado por la consigna
DB_NOMBRE = "mensajes.db"   # Archivo de la base SQLite


def crear_base_datos() -> None:
    """
    Crea la tabla 'mensajes' en la base SQLite si no existe.
    Campos: id, contenido, fecha_envio, ip_cliente.
    """
    try:
        conexion = sqlite3.connect(DB_NOMBRE)
        conexion.execute(
            """CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )"""
        )
        conexion.commit()
        conexion.close()
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo acceder a la base de datos: {error}")
        raise


def inicializar_socket() -> socket.socket:
    """
    Crea el socket TCP/IP y lo vincula a localhost:5000.
    """
    # Configuración del socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor.bind((HOST, PORT))
        servidor.listen(1)
        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
    except OSError as error:
        print(f"[ERROR] No se pudo iniciar el servidor en {HOST}:{PORT} "
              f"(puerto ocupado o sin permisos): {error}")
        servidor.close()
        raise
    return servidor


def guardar_mensaje(contenido: str, ip_cliente: str) -> None:
    """
    Guarda un mensaje en la base SQLite con su fecha de envío.
    """
    try:
        conexion = sqlite3.connect(DB_NOMBRE)
        conexion.execute(
            "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) "
            "VALUES (?, ?, ?)",
            (contenido, datetime.now().isoformat(timespec="seconds"), ip_cliente),
        )
        conexion.commit()
        conexion.close()
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo guardar el mensaje: {error}")


def aceptar_conexiones(servidor: socket.socket) -> None:
    """
    Acepta conexiones entrantes, recibe los mensajes del cliente,
    los guarda en la DB y envía la confirmación.
    """
    while True:
        try:
            # Acepta una conexión entrante
            conexion, direccion = servidor.accept()
            print(f"[SERVIDOR] Conexión establecida desde {direccion}")
        except OSError as error:
            print(f"[ERROR] Fallo al aceptar conexión: {error}")
            return

        with conexion:
            while True:
                # Recibe el mensaje del cliente (hasta 1024 bytes)
                datos = conexion.recv(1024).decode("utf-8")
                if not datos:
                    break  # Cliente cerró la conexión

                print(f"[SERVIDOR] Mensaje recibido de {direccion}: {datos}")
                guardar_mensaje(datos, direccion[0])

                # Respuesta con el timestamp de recepción
                respuesta = f"Mensaje recibido: {datetime.now().isoformat(timespec='seconds')}"
                conexion.sendall(respuesta.encode("utf-8"))

        print("[SERVIDOR] Conexión cerrada.")


if __name__ == "__main__":
    crear_base_datos()
    servidor = inicializar_socket()
    try:
        aceptar_conexiones(servidor)
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Detenido por el usuario.")
    finally:
        servidor.close()