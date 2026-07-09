import mysql.connector as mysql
from config import DB_CONFIG


def connect():
    try:
        connection = mysql.connect(**DB_CONFIG)
        return connection
    except mysql.Error as err:
        print(err)
        return None


# ======================================
# BUSCAR PRODUCTOS PARA LA VENTA
# ======================================

def buscarProductoVenta(texto):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar.", []

    cursor = connection.cursor(dictionary=True)

    try:

        texto = f"%{texto}%"

        cursor.execute("""
            SELECT
                id_producto,
                codigo,
                nombre,
                precio_venta,
                stock
            FROM productos
            WHERE estado = 1
            AND stock > 0
            AND (
                nombre LIKE %s
                OR codigo LIKE %s
            )
            ORDER BY nombre
            LIMIT 10
        """, (
            texto,
            texto
        ))

        productos = cursor.fetchall()

        return True, "Productos encontrados.", productos

    except mysql.Error as err:

        print(err)

        return False, "Error al buscar productos.", []

    finally:

        cursor.close()
        connection.close()