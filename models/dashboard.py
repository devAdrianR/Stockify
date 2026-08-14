import mysql.connector as mysql
from config import DB_CONFIG


# =====================================================
# CONEXIÓN
# =====================================================

def connect():

    try:

        return mysql.connect(**DB_CONFIG)

    except mysql.Error as err:

        print("Error de conexión:", err)

        return None


# =====================================================
# OBTENER EMPRESA
# =====================================================

def obtenerEmpresa(id_empresa):

    connection = connect()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                id_empresa,
                nombre,
                nit,
                direccion,
                telefono,
                estado
            FROM empresas
            WHERE id_empresa = %s
            LIMIT 1
        """, (
            id_empresa,
        ))

        empresa = cursor.fetchone()

        return empresa

    except mysql.Error as err:

        print(
            "Error al obtener empresa:",
            err
        )

        return None

    finally:

        cursor.close()
        connection.close()