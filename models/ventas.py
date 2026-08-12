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
# BUSCAR PRODUCTOS PARA UNA VENTA
# =====================================================

def buscarProductoVenta(texto, id_empresa):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar.", []

    cursor = connection.cursor(dictionary=True)

    try:

        texto = f"%{texto}%"

        cursor.execute("""
            SELECT
                id_empresa,
                id_producto,
                codigo,
                nombre,
                precio_venta,
                stock
            FROM productos
            WHERE estado = 1
            AND stock > 0
            AND id_empresa = %s
            AND (
                nombre LIKE %s
                OR codigo LIKE %s
            )
            ORDER BY nombre
            LIMIT 10
        """, (
            id_empresa,
            texto,
            texto
        ))

        productos = cursor.fetchall()

        return True, "Productos encontrados.", productos

    except mysql.Error as err:

        print("Error al buscar productos:", err)

        return False, "Error al buscar productos.", []

    finally:

        cursor.close()
        connection.close()


# =====================================================
# REGISTRAR VENTA
# =====================================================

def registrarVenta(
    id_empresa,
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
        return False, "No fue posible conectar.", None

    cursor = connection.cursor()

    try:

        connection.start_transaction()

        # =============================================
        # CREAR CABECERA DE LA VENTA
        # =============================================

        cursor.execute("""
            INSERT INTO ventas
            (
                id_usuario,
                id_empresa,
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
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'Completada'
            )
        """, (
            id_usuario,
            id_empresa,
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


        # =============================================
        # PROCESAR PRODUCTOS
        # =============================================

        for producto in productos:

            id_producto = producto["id_producto"]

            cantidad = int(
                producto["cantidad"]
            )

            precio = producto["precio"]

            subtotal_producto = producto["subtotal"]


            if cantidad <= 0:
                raise Exception(
                    "La cantidad del producto debe ser mayor que cero."
                )


            # =========================================
            # CONSULTAR Y BLOQUEAR STOCK
            # =========================================

            cursor.execute("""
                SELECT
                    stock,
                    nombre
                FROM productos
                WHERE id_producto = %s
                AND id_empresa = %s
                FOR UPDATE
            """, (
                id_producto,
                id_empresa
            ))

            resultado = cursor.fetchone()


            if resultado is None:

                raise Exception(
                    "Producto inexistente."
                )


            stock = resultado[0]

            nombre_producto = resultado[1]


            # =========================================
            # VALIDAR STOCK
            # =========================================

            if cantidad > stock:

                raise Exception(
                    f"Stock insuficiente para {nombre_producto}."
                )


            # =========================================
            # INSERTAR DETALLE
            # =========================================

            cursor.execute("""
                INSERT INTO detalle_venta
                (
                    id_venta,
                    id_producto,
                    cantidad,
                    precio,
                    subtotal,
                    id_empresa
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                id_venta,
                id_producto,
                cantidad,
                precio,
                subtotal_producto,
                id_empresa
            ))


            # =========================================
            # ACTUALIZAR STOCK
            # =========================================

            cursor.execute("""
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s
                AND id_empresa = %s
            """, (
                cantidad,
                id_producto,
                id_empresa
            ))


        # =============================================
        # CONFIRMAR TRANSACCIÓN
        # =============================================

        connection.commit()

        return (
            True,
            "Venta registrada correctamente.",
            id_venta
        )


    except Exception as err:

        connection.rollback()

        print(
            "Error al registrar venta:",
            err
        )

        return (
            False,
            str(err),
            None
        )


    finally:

        cursor.close()
        connection.close()


# =====================================================
# OBTENER VENTA PARA FACTURA
# =====================================================

def obtenerVentaFactura(id_empresa, id_venta):

    connection = connect()

    if connection is None:
        return None, []

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        # =============================================
        # CABECERA
        # =============================================

        cursor.execute("""
            SELECT

                v.id_venta,
                v.id_empresa,
                v.id_usuario,
                v.cliente,
                v.documento,
                v.fecha,
                v.metodo_pago,
                v.subtotal,
                v.descuento,
                v.iva,
                v.total,
                v.observaciones,
                v.estado

            FROM ventas v

            WHERE v.id_venta = %s
            AND v.id_empresa = %s

            LIMIT 1
        """, (
            id_venta,
            id_empresa
        ))

        venta = cursor.fetchone()


        if venta is None:

            return None, []


        # =============================================
        # DETALLE
        # =============================================

        cursor.execute("""
            SELECT

                p.codigo,
                p.nombre,

                dv.cantidad,
                dv.precio,
                dv.subtotal

            FROM detalle_venta dv

            INNER JOIN productos p
                ON p.id_producto = dv.id_producto
                AND p.id_empresa = dv.id_empresa

            WHERE dv.id_venta = %s
            AND dv.id_empresa = %s

            ORDER BY dv.id_detalle ASC
        """, (
            id_venta,
            id_empresa
        ))

        productos = cursor.fetchall()


        return venta, productos


    except mysql.Error as err:

        print(
            "Error al obtener factura:",
            err
        )

        return None, []


    finally:

        cursor.close()
        connection.close()