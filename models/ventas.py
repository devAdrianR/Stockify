import mysql.connector as mysql
from config import DB_CONFIG


def connect():

    try:

        return mysql.connect(**DB_CONFIG)

    except mysql.Error as err:

        print(err)

        return None


# ==========================================
# BUSCAR PRODUCTOS
# ==========================================

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


# ==========================================
# REGISTRAR VENTA
# ==========================================

def registrarVenta(
        id_usuario,
        cliente,
        documento,
        fecha,
        metodo_pago,
        subtotal,
        descuento,
        iva,
        total,
        observaciones,
        productos
):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar."

    cursor = connection.cursor()

    try:

        connection.start_transaction()

        cursor.execute("""

            INSERT INTO ventas
            (

                id_usuario,
                cliente,
                documento,
                fecha,
                metodo_pago,
                subtotal,
                descuento,
                iva,
                total,
                observaciones,
                estado

            )

            VALUES

            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)

        """, (

            id_usuario,
            cliente,
            documento,
            fecha,
            metodo_pago,
            subtotal,
            descuento,
            iva,
            total,
            observaciones

        ))

        id_venta = cursor.lastrowid

        #========================================

        for producto in productos:

            cursor.execute("""

                SELECT stock
                FROM productos
                WHERE id_producto=%s

            """, (

                producto["id_producto"],

            ))

            resultado = cursor.fetchone()

            if resultado is None:

                raise Exception("Producto inexistente.")

            stock = resultado[0]

            if producto["cantidad"] > stock:

                raise Exception(
                    f"Stock insuficiente para {producto['nombre']}"
                )

            cursor.execute("""

                INSERT INTO detalle_venta
                (

                    id_venta,
                    id_producto,
                    cantidad,
                    precio,
                    subtotal

                )

                VALUES

                (%s,%s,%s,%s,%s)

            """, (

                id_venta,
                producto["id_producto"],
                producto["cantidad"],
                producto["precio"],
                producto["subtotal"]

            ))

            cursor.execute("""

                UPDATE productos

                SET stock = stock - %s

                WHERE id_producto = %s

            """, (

                producto["cantidad"],
                producto["id_producto"]

            ))

        connection.commit()

        return True, "Venta registrada correctamente."

    except Exception as err:

        connection.rollback()

        print(err)

        return False, str(err)

    finally:

        cursor.close()
        connection.close()