import mysql.connector as mysql
from config import DB_CONFIG
from datetime import date


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
# RESUMEN GENERAL DE REPORTES
# =====================================================

def resumenReportes(id_empresa):

    connection = connect()

    if connection is None:

        return {
            "reportes": 5,
            "ventas_mes": 0,
            "productos": 0,
            "mas_vendido": "---"
        }

    cursor = connection.cursor(dictionary=True)

    try:

        # =================================================
        # PRODUCTOS REGISTRADOS
        # =================================================

        cursor.execute("""
            SELECT COUNT(*) AS total

            FROM productos

            WHERE id_empresa = %s

        """, (
            id_empresa,
        ))

        resultado = cursor.fetchone()

        productos = resultado["total"] or 0


        # =================================================
        # VENTAS DEL MES
        # =================================================

        cursor.execute("""
            SELECT

                COALESCE(SUM(total), 0) AS total

            FROM ventas

            WHERE id_empresa = %s

            AND estado = 'Completada'

            AND MONTH(fecha) = MONTH(CURDATE())

            AND YEAR(fecha) = YEAR(CURDATE())

        """, (
            id_empresa,
        ))

        resultado = cursor.fetchone()

        ventas_mes = float(
            resultado["total"] or 0
        )


        # =================================================
        # PRODUCTO MÁS VENDIDO
        # =================================================

        cursor.execute("""
            SELECT

                p.nombre,

                SUM(dv.cantidad) AS cantidad

            FROM detalle_venta dv

            INNER JOIN productos p

                ON p.id_producto = dv.id_producto

                AND p.id_empresa = dv.id_empresa

            INNER JOIN ventas v

                ON v.id_venta = dv.id_venta

                AND v.id_empresa = dv.id_empresa

            WHERE dv.id_empresa = %s

            AND v.estado = 'Completada'

            GROUP BY

                p.id_producto,

                p.nombre

            ORDER BY cantidad DESC

            LIMIT 1

        """, (
            id_empresa,
        ))

        producto = cursor.fetchone()

        if producto:

            mas_vendido = producto["nombre"]

        else:

            mas_vendido = "---"


        return {

            "reportes": 5,

            "ventas_mes": ventas_mes,

            "productos": productos,

            "mas_vendido": mas_vendido

        }


    except mysql.Error as err:

        print("Error resumenReportes:", err)

        return {

            "reportes": 5,

            "ventas_mes": 0,

            "productos": 0,

            "mas_vendido": "---"

        }


    finally:

        cursor.close()
        connection.close()


# =====================================================
# VENTAS DIARIAS
# =====================================================

def ventasDiarias(id_empresa, fecha=None):

    connection = connect()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:

        if not fecha:
            fecha = date.today()

        cursor.execute("""
            SELECT

                v.id_venta,
                v.cliente,
                v.documento,
                v.fecha,
                v.metodo_pago,
                v.subtotal,
                v.descuento,
                v.iva,
                v.total,
                v.observaciones,
                v.id_usuario,
                v.estado,

                -- Cantidad total de unidades vendidas
                COALESCE(SUM(dv.cantidad), 0) AS productos,

                -- Nombre del usuario que realizó la venta
                u.nombre_usuario

            FROM ventas v

            LEFT JOIN detalle_venta dv
                ON dv.id_venta = v.id_venta
                AND dv.id_empresa = v.id_empresa

            LEFT JOIN usuarios u
                ON u.id_usuario = v.id_usuario
                AND u.id_empresa = v.id_empresa

            WHERE v.id_empresa = %s
            AND DATE(v.fecha) = %s
            AND v.estado = 'Completada'

            GROUP BY
                v.id_venta,
                v.cliente,
                v.documento,
                v.fecha,
                v.metodo_pago,
                v.subtotal,
                v.descuento,
                v.iva,
                v.total,
                v.observaciones,
                v.id_usuario,
                v.estado,
                u.nombre_usuario

            ORDER BY v.fecha DESC

        """, (
            id_empresa,
            fecha
        ))

        ventas = cursor.fetchall()

        return ventas

    except mysql.Error as err:

        print("Error ventasDiarias:", err)

        return []

    finally:

        cursor.close()
        connection.close()


# =====================================================
# RESUMEN DE VENTAS DIARIAS
# =====================================================

def resumenVentasDiarias(id_empresa, fecha=None):

    connection = connect()

    if connection is None:

        return {

            "total_ventas": 0,

            "ingresos": 0,

            "productos": 0,

            "promedio": 0

        }

    cursor = connection.cursor(dictionary=True)

    try:

        if not fecha:

            fecha = date.today()


        # =================================================
        # VENTAS / INGRESOS / PROMEDIO
        # =================================================

        cursor.execute("""
            SELECT

                COUNT(*) AS total_ventas,

                COALESCE(SUM(total), 0) AS ingresos,

                COALESCE(AVG(total), 0) AS promedio

            FROM ventas

            WHERE id_empresa = %s

            AND DATE(fecha) = %s

            AND estado = 'Completada'

        """, (
            id_empresa,
            fecha
        ))

        resumen = cursor.fetchone()


        # =================================================
        # PRODUCTOS VENDIDOS
        # =================================================

        cursor.execute("""
            SELECT

                COALESCE(SUM(dv.cantidad), 0) AS productos

            FROM detalle_venta dv

            INNER JOIN ventas v

                ON v.id_venta = dv.id_venta

                AND v.id_empresa = dv.id_empresa

            WHERE v.id_empresa = %s

            AND DATE(v.fecha) = %s

            AND v.estado = 'Completada'

        """, (
            id_empresa,
            fecha
        ))

        productos = cursor.fetchone()


        return {

            "total_ventas":
                resumen["total_ventas"] or 0,

            "ingresos":
                float(resumen["ingresos"] or 0),

            "productos":
                productos["productos"] or 0,

            "promedio":
                float(resumen["promedio"] or 0)

        }


    except mysql.Error as err:

        print("Error resumenVentasDiarias:", err)

        return {

            "total_ventas": 0,

            "ingresos": 0,

            "productos": 0,

            "promedio": 0

        }


    finally:

        cursor.close()
        connection.close()


# =====================================================
# DETALLE DE UNA VENTA
# =====================================================

def detalleVenta(id_empresa, id_venta):

    connection = connect()

    if connection is None:

        return None, []

    cursor = connection.cursor(dictionary=True)

    try:

        # =================================================
        # ENCABEZADO DE LA VENTA
        # =================================================

        cursor.execute("""
            SELECT

                v.id_venta,

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

        """, (
            id_venta,
            id_empresa
        ))

        venta = cursor.fetchone()


        if venta is None:

            return None, []


        # =================================================
        # PRODUCTOS DE LA VENTA
        # =================================================

        cursor.execute("""
            SELECT

                p.codigo,

                p.nombre,

                p.categoria,

                dv.cantidad,

                dv.precio,

                dv.subtotal

            FROM detalle_venta dv

            INNER JOIN productos p

                ON p.id_producto = dv.id_producto

                AND p.id_empresa = dv.id_empresa

            WHERE dv.id_venta = %s

            AND dv.id_empresa = %s

            ORDER BY p.nombre

        """, (
            id_venta,
            id_empresa
        ))

        productos = cursor.fetchall()


        return venta, productos


    except mysql.Error as err:

        print("Error detalleVenta:", err)

        return None, []


    finally:

        cursor.close()
        connection.close()

# =====================================================
# PRODUCTOS MÁS VENDIDOS
# =====================================================

def productosMasVendidos(id_empresa, fecha_inicio=None, fecha_fin=None):

    connection = connect()

    if connection is None:
        return {
            "resumen": {
                "producto_mas_vendido": "Sin datos",
                "unidades_vendidas": 0,
                "productos_diferentes": 0,
                "ingresos": 0
            },
            "productos": []
        }

    cursor = connection.cursor(dictionary=True)

    try:

        # =================================================
        # CONSULTA PRINCIPAL
        # =================================================

        query = """
            SELECT

                p.id_producto,

                p.codigo,

                p.nombre AS nombre_producto,

                p.categoria,

                SUM(dv.cantidad) AS cantidad_vendida,

                COALESCE(
                    SUM(dv.subtotal),
                    0
                ) AS ingresos,

                COALESCE(
                    SUM(dv.subtotal) /
                    NULLIF(SUM(dv.cantidad), 0),
                    0
                ) AS precio_promedio

            FROM detalle_venta dv

            INNER JOIN ventas v
                ON v.id_venta = dv.id_venta
                AND v.id_empresa = dv.id_empresa

            INNER JOIN productos p
                ON p.id_producto = dv.id_producto
                AND p.id_empresa = dv.id_empresa

            WHERE dv.id_empresa = %s

            AND v.estado = 'Completada'
        """

        parametros = [id_empresa]


        # =================================================
        # FILTRO FECHA INICIAL
        # =================================================

        if fecha_inicio:

            query += """
                AND DATE(v.fecha) >= %s
            """

            parametros.append(fecha_inicio)


        # =================================================
        # FILTRO FECHA FINAL
        # =================================================

        if fecha_fin:

            query += """
                AND DATE(v.fecha) <= %s
            """

            parametros.append(fecha_fin)


        # =================================================
        # AGRUPAR Y ORDENAR
        # =================================================

        query += """

            GROUP BY
                p.id_producto,
                p.codigo,
                p.nombre,
                p.categoria

            ORDER BY
                cantidad_vendida DESC,
                ingresos DESC

        """


        # =================================================
        # EJECUTAR CONSULTA
        # =================================================

        cursor.execute(
            query,
            tuple(parametros)
        )

        productos = cursor.fetchall()


        # =================================================
        # CONVERTIR VALORES NUMÉRICOS
        # =================================================

        for producto in productos:

            producto["cantidad_vendida"] = int(
                producto["cantidad_vendida"] or 0
            )

            producto["ingresos"] = float(
                producto["ingresos"] or 0
            )

            producto["precio_promedio"] = float(
                producto["precio_promedio"] or 0
            )


        # =================================================
        # RESUMEN DEL PRODUCTO MÁS VENDIDO
        # =================================================

        if productos:

            # El primer producto es el que más unidades vendió
            producto_mas_vendido = productos[0]


            nombre_producto = producto_mas_vendido[
                "nombre_producto"
            ]


            unidades_vendidas = producto_mas_vendido[
                "cantidad_vendida"
            ]


            ingresos = producto_mas_vendido[
                "ingresos"
            ]


            # Cantidad de productos diferentes que aparecen
            # en el ranking completo
            productos_diferentes = len(productos)

        else:

            nombre_producto = "Sin datos"

            unidades_vendidas = 0

            ingresos = 0

            productos_diferentes = 0


        # =================================================
        # RETORNAR RESULTADO
        # =================================================

        return {

            "resumen": {

                "producto_mas_vendido":
                    nombre_producto,

                "unidades_vendidas":
                    unidades_vendidas,

                "productos_diferentes":
                    productos_diferentes,

                "ingresos":
                    ingresos

            },

            "productos":
                productos

        }


    # =====================================================
    # ERROR MYSQL
    # =====================================================

    except mysql.Error as err:

        print(
            "Error productosMasVendidos:",
            err
        )

        return {

            "resumen": {

                "producto_mas_vendido":
                    "Sin datos",

                "unidades_vendidas":
                    0,

                "productos_diferentes":
                    0,

                "ingresos":
                    0

            },

            "productos": []

        }


    # =====================================================
    # CERRAR CONEXIÓN
    # =====================================================

    finally:

        cursor.close()

        connection.close()