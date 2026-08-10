import mysql.connector
from config import DB_CONFIG


def connect():
    return mysql.connector.connect(**DB_CONFIG)


def registrar_ingreso(concepto, monto, categoria, fecha, descripcion):
    conn = None
    cursor = None

    try:
        conn = connect()
        cursor = conn.cursor()

        sql = """
            INSERT INTO ingresos
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
        conn.commit()

        return True, "Ingreso registrado correctamente."

    except mysql.connector.Error as e:
        if conn:
            conn.rollback()

        return False, f"Error al registrar el ingreso: {e}"

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()


def obtener_ingresos():
    conn = None
    cursor = None

    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM ingresos
            ORDER BY fecha DESC, id_ingreso DESC
        """)

        ingresos = cursor.fetchall()

        return True, ingresos

    except mysql.connector.Error as e:
        return False, f"Error al consultar ingresos: {e}"

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()