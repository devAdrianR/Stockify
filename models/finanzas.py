import mysql.connector as mysql
from config import DB_CONFIG


def connect():

    try:

        return mysql.connect(**DB_CONFIG)

    except mysql.Error as err:

        print(err)

        return None


# ==========================================
# REGISTRAR MOVIMIENTO
# ==========================================

def registrarMovimiento(
        id_usuario,
        tipo,
        concepto,
        monto,
        categoria,
        fecha,
        descripcion
):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        cursor.execute("""

            INSERT INTO finanzas
            (

                id_usuario,
                tipo,
                concepto,
                monto,
                categoria,
                fecha,
                descripcion,
                estado

            )

            VALUES

            (%s,%s,%s,%s,%s,%s,%s,1)

        """, (

            id_usuario,
            tipo,
            concepto,
            monto,
            categoria,
            fecha,
            descripcion

        ))

        connection.commit()

        return True, "Movimiento registrado correctamente."

    except Exception as err:

        connection.rollback()

        print(err)

        return False, str(err)

    finally:

        cursor.close()
        connection.close()


# ==========================================
# LISTAR MOVIMIENTOS
# ==========================================

def listarMovimientos(id_usuario):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar.", []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""

            SELECT

                id_movimiento,
                tipo,
                concepto,
                monto,
                categoria,
                fecha,
                descripcion

            FROM finanzas

            WHERE estado = 1
            AND id_usuario = %s

            ORDER BY fecha DESC,
                     id_movimiento DESC

        """, (

            id_usuario,

        ))

        movimientos = cursor.fetchall()

        return True, "Movimientos encontrados.", movimientos

    except Exception as err:

        print(err)

        return False, str(err), []

    finally:

        cursor.close()
        connection.close()