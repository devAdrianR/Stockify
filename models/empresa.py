import mysql.connector as mysql
from config import DB_CONFIG


def connect():

    try:

        return mysql.connect(**DB_CONFIG)

    except mysql.Error as err:

        print(err)

        return None


# ==========================================
# REGISTRAR EMPRESA
# ==========================================

def registrarEmpresa(
        nombre,
        nit,
        direccion,
        telefono,
        estado
):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT id_empresa
        FROM empresas
        WHERE nombre=%s
        OR nit=%s

    """, (

        nombre,
        nit

    ))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "La empresa ya existe."

    cursor.close()

    cursor = connection.cursor()

    try:

        cursor.execute("""

            INSERT INTO empresas
            (

                nombre,
                nit,
                direccion,
                telefono,
                estado

            )

            VALUES

            (%s,%s,%s,%s,%s)

        """, (

            nombre,
            nit,
            direccion,
            telefono,
            estado

        ))

        connection.commit()

        return True, "Empresa registrada correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible registrar la empresa."

    finally:

        cursor.close()
        connection.close()


# ==========================================
# OBTENER EMPRESAS
# ==========================================

def obtenerEmpresas():

    connection = connect()

    if connection is None:

        return []

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *
        FROM empresas
        ORDER BY nombre

    """)

    empresas = cursor.fetchall()

    cursor.close()
    connection.close()

    return empresas


# ==========================================
# OBTENER EMPRESA POR ID
# ==========================================

def obtenerEmpresaID(id_empresa):

    connection = connect()

    if connection is None:

        return None

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT *
        FROM empresas
        WHERE id_empresa=%s

    """, (

        id_empresa,

    ))

    empresa = cursor.fetchone()

    cursor.close()
    connection.close()

    return empresa


# ==========================================
# ACTUALIZAR EMPRESA
# ==========================================

def actualizarEmpresa(
        id_empresa,
        nombre,
        nit,
        direccion,
        telefono,
        estado
):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""

        SELECT id_empresa
        FROM empresas
        WHERE (nombre=%s OR nit=%s)
        AND id_empresa<>%s

    """, (

        nombre,
        nit,
        id_empresa

    ))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "Ya existe una empresa con esos datos."

    cursor.close()

    cursor = connection.cursor()

    try:

        cursor.execute("""

            UPDATE empresas

            SET

                nombre=%s,
                nit=%s,
                direccion=%s,
                telefono=%s,
                estado=%s

            WHERE id_empresa=%s

        """, (

            nombre,
            nit,
            direccion,
            telefono,
            estado,
            id_empresa

        ))

        connection.commit()

        return True, "Empresa actualizada correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible actualizar la empresa."

    finally:

        cursor.close()
        connection.close()


# ==========================================
# ACTIVAR EMPRESA
# ==========================================

def activarEmpresa(id_empresa):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        cursor.execute("""

            UPDATE empresas

            SET estado=1

            WHERE id_empresa=%s

        """, (

            id_empresa,

        ))

        connection.commit()

        return True, "Empresa activada correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible activar la empresa."

    finally:

        cursor.close()
        connection.close()


# ==========================================
# DESACTIVAR EMPRESA
# ==========================================

def desactivarEmpresa(id_empresa):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        cursor.execute("""

            UPDATE empresas

            SET estado=0

            WHERE id_empresa=%s

        """, (

            id_empresa,

        ))

        connection.commit()

        return True, "Empresa desactivada correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible desactivar la empresa."

    finally:

        cursor.close()
        connection.close()