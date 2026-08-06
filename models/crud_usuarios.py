import mysql.connector as mysql
from config import DB_CONFIG
from werkzeug.security import generate_password_hash


def connect():

    try:
        return mysql.connect(**DB_CONFIG)
    except mysql.Error as err:
        print(err)
        return None


# =====================================
# EMPRESAS
# =====================================

def obtenerEmpresas():

    connection = connect()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM empresas

        WHERE estado = 1

        ORDER BY nombre

    """)

    empresas = cursor.fetchall()

    cursor.close()
    connection.close()

    return empresas


# =====================================
# OBTENER USUARIOS
# =====================================

def obtenerUsuarios():

    connection = connect()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT
            u.*,
            e.nombre AS empresa

        FROM usuarios u

        LEFT JOIN empresas e
            ON u.id_empresa = e.id_empresa

        WHERE u.rol <> 'SUPERADMIN'

        ORDER BY u.fecha_creacion DESC

    """)

    usuarios = cursor.fetchall()

    cursor.close()
    connection.close()

    return usuarios


# =====================================
# OBTENER USUARIO POR ID
# =====================================

def obtenerUsuarioID(id_usuario):

    connection = connect()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *

        FROM usuarios

        WHERE id_usuario=%s

        AND rol<>'SUPERADMIN'

    """, (id_usuario,))

    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    return usuario


# =====================================
# REGISTRAR
# =====================================

def registrarUsuario(nombre_usuario,
                     correo,
                     password,
                     rol,
                     id_empresa):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT id_usuario

        FROM usuarios

        WHERE nombre_usuario=%s
        OR correo=%s

    """, (nombre_usuario, correo))

    
    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "El usuario o correo ya existen."

    cursor.close()

    cursor = connection.cursor()

    password = generate_password_hash(password)

    try:

        cursor.execute("""

            INSERT INTO usuarios(

                nombre_usuario,
                correo,
                password,
                rol,
                id_empresa,
                estado

            )

            VALUES(%s,%s,%s,%s,%s,1)

        """, (

            nombre_usuario,
            correo,
            password,
            rol,
            id_empresa if id_empresa else None

        ))

        connection.commit()

        return True, "Usuario registrado."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible registrar."

    finally:

        cursor.close()
        connection.close()


# =====================================
# ACTUALIZAR
# =====================================

def actualizarUsuario(id_usuario,
                      nombre_usuario,
                      correo,
                      password,
                      rol,
                      id_empresa,
                      estado):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT id_usuario

        FROM usuarios

        WHERE (nombre_usuario=%s OR correo=%s)

        AND id_usuario<>%s

    """, (

        nombre_usuario,
        correo,
        id_usuario

    ))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "Usuario o correo ya existen."

    cursor.close()

    cursor = connection.cursor()

    try:

        if password != "":

            password = generate_password_hash(password)

            cursor.execute("""

                UPDATE usuarios

                SET

                    nombre_usuario=%s,
                    correo=%s,
                    password=%s,
                    rol=%s,
                    id_empresa=%s,
                    estado=%s

                WHERE id_usuario=%s

            """, (

                nombre_usuario,
                correo,
                password,
                rol,
                id_empresa if id_empresa else None,
                estado,
                id_usuario

            ))

        else:

            cursor.execute("""

                UPDATE usuarios

                SET

                    nombre_usuario=%s,
                    correo=%s,
                    rol=%s,
                    id_empresa=%s,
                    estado=%s

                WHERE id_usuario=%s

            """, (

                nombre_usuario,
                correo,
                rol,
                id_empresa if id_empresa else None,
                estado,
                id_usuario

            ))

        connection.commit()

        return True, "Usuario actualizado."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible actualizar."

    finally:

        cursor.close()
        connection.close()


# =====================================
# ACTIVAR
# =====================================

def activarUsuario(id_usuario):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        cursor.execute("""

            UPDATE usuarios

            SET estado=1

            WHERE id_usuario=%s

            AND rol<>'SUPERADMIN'

        """, (id_usuario,))

        connection.commit()

        return True, "Usuario activado."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible activar."

    finally:

        cursor.close()
        connection.close()


# =====================================
# DESACTIVAR
# =====================================

def desactivarUsuario(id_usuario):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        cursor.execute("""

            UPDATE usuarios

            SET estado=0

            WHERE id_usuario=%s

            AND rol<>'SUPERADMIN'

        """, (id_usuario,))

        connection.commit()

        return True, "Usuario desactivado."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible desactivar."

    finally:

        cursor.close()
        connection.close()