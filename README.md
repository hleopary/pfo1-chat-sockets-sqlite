# PFO 1 - Chat básico cliente-servidor con sockets y SQLite

**Repositorio (entrega):** https://github.com/hleopary/pfo1-chat-sockets-sqlite

**Materia:** Programación sobre Redes (3.1.1) · IFTS29
**Práctica Formativa Obligatoria 1** · Ciclo 2026
**Autor:** Leandro Paryszewski
**Fecha:** 20/09/2026

---

## Descripción

Implementación de un chat básico cliente-servidor usando **sockets TCP** en Python, con **persistencia en SQLite** y buena práctica de modularización y manejo de errores, según la consigna de `apuntes/PFO 1- 1C Programación sobre redes_2026.pdf`.

- `server.py` — escucha en `localhost:5000`, recibe mensajes, los guarda en una base SQLite y responde `"Mensaje recibido: <timestamp>"`.
- `client.py` — se conecta al servidor, envía mensajes hasta que el usuario escribe `éxito` y muestra la respuesta de cada envío.

## Estructura del proyecto

```
pfo1_chat_sockets_sqlite/
├── server.py      ← Servidor: socket TCP + SQLite + manejo de errores
├── client.py      ← Cliente: envía mensajes hasta 'éxito'
├── README.md      ← Este documento de entrega
└── .gitignore     ← Excluye DB, logs y caché
```

## Requisitos

- Python 3.11+ (probado con 3.14).
- Solo **librería estándar** (`socket`, `sqlite3`, `datetime`). No requiere instalar nada.

## Cómo ejecutar

### 1. Iniciar el servidor (Terminal 1)

```bash
python3 server.py
```

Salida esperada:

```
[SERVIDOR] Escuchando en localhost:5000...
```

### 2. Iniciar el cliente (Terminal 2)

```bash
python3 client.py
```

Ejemplo de sesión:

```
$ python3 client.py
[CLIENTE] Conectado al servidor localhost:5000
Escribí tu mensaje (o 'éxito' para salir): hola servidor
[CLIENTE] Respuesta del servidor: Mensaje recibido: 2026-09-20T23:37:21
Escribí tu mensaje (o 'éxito' para salir): segundo mensaje
[CLIENTE] Respuesta del servidor: Mensaje recibido: 2026-09-20T23:37:22
Escribí tu mensaje (o 'éxito' para salir): éxito
[CLIENTE] Terminando la conexión.
```

## Evidencia de prueba (20/09/2026)

Prueba end-to-end con un solo cliente:

```
# Servidor
[SERVIDOR] Escuchando en localhost:5000...
[SERVIDOR] Conexión establecida desde ('127.0.0.1', 58408)
[SERVIDOR] Mensaje recibido de ('127.0.0.1', 58408): primer mensaje
[SERVIDOR] Conexión cerrada.

# Datos persistidos (mensajes.db)
$ sqlite3 mensajes.db "SELECT * FROM mensajes;"
1|primer mensaje|2026-09-20T23:37:27|127.0.0.1
```

### Caso de error verificado: puerto ocupado

```
[ERROR] No se pudo iniciar el servidor en localhost:5000 (puerto ocupado o sin permisos): [Errno 98] Address already in use
```

## Requisitos de la consigna (y cómo se cumplen)

| Requisito | Implementación |
|-----------|----------------|
| Socket que escuche en `localhost:5000` | `inicializar_socket()` → `bind((HOST, PORT))` + `listen()` |
| Funciones separadas | `crear_base_datos()`, `inicializar_socket()`, `aceptar_conexiones()`, `guardar_mensaje()` |
| Guardar en DB con `id, contenido, fecha_envio, ip_cliente` | `guardar_mensaje()` inserta los 4 campos |
| Manejar errores (puerto ocupado, DB no accesible) | `try/except` con `OSError` y `sqlite3.Error` |
| Responder `"Mensaje recibido: <timestamp>"` | Confirmación en `aceptar_conexiones()` con `datetime.now()` |
| Cliente envía varios mensajes hasta `éxito` | Bucle `while` en `client.py` que corta con `éxito` |
| Mostrar respuesta del servidor por mensaje | `client.py` imprime la respuesta de cada envío |
| Comentarios en cada sección clave | Servidor y cliente comentados en español |

## Base de datos (SQLite)

Tabla `mensajes` en `mensajes.db` (se crea automáticamente al iniciar el servidor):

| Campo         | Tipo          | Descripción                      |
|---------------|---------------|----------------------------------|
| `id`          | INTEGER PK    | Identificador autoincremental    |
| `contenido`   | TEXT          | Mensaje del cliente              |
| `fecha_envio` | TEXT (ISO)    | Fecha/hora de recepción          |
| `ip_cliente`  | TEXT          | Dirección IP del cliente         |

Consultar los datos guardados:

```bash
sqlite3 mensajes.db "SELECT * FROM mensajes;"
```

## Errores comunes

- **`Address already in use`** → el puerto está ocupado; cerra el proceso anterior del servidor o cambiá `PORT`.
- **`Connection refused`** → el servidor no está corriendo; iniciá `server.py` primero.
- **`mensajes.db` bloqueado** → otro proceso escribiendo; cerrá la sesión anterior.

## Entrega

- Subir **repositorio** (GitHub/Bitbucket) **o** archivo comprimido (`.zip`/`.rar`) con esta carpeta.
- Incluir este README y la evidencia de prueba.