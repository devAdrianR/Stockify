import mysql.connector
from config import DB_CONFIG


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


def registrar_gasto(concepto, monto, categoria, fecha, descripcion):
    conexion = None
    cursor = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO gastos
            (concepto, monto, categoria, fecha, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            concepto,
            monto,
            categoria,
            fecha,
            descripcion
        )

        cursor.execute(sql, valores)
        conexion.commit()

        return True, "Gasto registrado correctamente."

    except mysql.connector.Error as e:

        if conexion:
            conexion.rollback()

        return False, f"Error al registrar el gasto: {e}"

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()


def obtener_gastos():
    conexion = None
    cursor = None

    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM gastos
            ORDER BY fecha DESC, id_gasto DESC
        """)

        gastos = cursor.fetchall()

        return True, gastos

    except mysql.connector.Error as e:

        return False, f"Error al consultar gastos: {e}"

    finally:

        if cursor:
            cursor.close()

        if conexion:
            conexion.close()