import mysql.connector as mysql
from config import DB_CONFIG


def connect():
    try:
        connection = mysql.connect(**DB_CONFIG)
        return connection
    except mysql.Error as err:
        print(err)
        return None


# ==========================
# REGISTRAR PRODUCTO
# ==========================

def registrarProducto(id_empresa, nombre, codigo, categoria, costo, precio_venta, stock, descripcion):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_producto
        FROM productos
        WHERE id_empresa=%s
        AND (nombre=%s OR codigo=%s)
    """, (id_empresa, nombre, codigo))

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return False, "El nombre o el código del producto ya existen."

    cursor.close()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO productos
            (id_empresa,nombre,codigo,categoria,costo,precio_venta,stock,descripcion)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            id_empresa,
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion
        ))

        connection.commit()

        return True, "Producto registrado correctamente."

    except mysql.Error as err:

        print(err)
        return False, "No fue posible registrar el producto."

    finally:

        cursor.close()
        connection.close()


# ==========================
# OBTENER PRODUCTOS
# ==========================

def obtenerProducto(id_empresa, id_producto=None):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos.", None

    cursor = connection.cursor(dictionary=True)

    try:

        if id_producto is None:

            cursor.execute("""
                SELECT *
                FROM productos
                WHERE id_empresa=%s
                ORDER BY nombre
            """, (id_empresa,))

            productos = cursor.fetchall()

            return True, "Productos obtenidos correctamente.", productos

        cursor.execute("""
            SELECT *
            FROM productos
            WHERE id_producto=%s
            AND id_empresa=%s
        """, (id_producto, id_empresa))

        producto = cursor.fetchone()

        if producto is None:
            return False, "Producto no encontrado.", None

        return True, "Producto obtenido correctamente.", producto

    except mysql.Error as err:

        print(err)

        return False, "No fue posible obtener los productos.", None

    finally:

        cursor.close()
        connection.close()


# ==========================
# EDITAR PRODUCTO
# ==========================

def editarProducto(
    id_empresa,
    id_producto,
    nombre,
    codigo,
    categoria,
    costo,
    precio_venta,
    stock,
    descripcion,
    estado
):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_producto
        FROM productos
        WHERE id_empresa=%s
        AND (nombre=%s OR codigo=%s)
        AND id_producto<>%s
    """, (
        id_empresa,
        nombre,
        codigo,
        id_producto
    ))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False, "El nombre o el código ya existen."

    cursor.close()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE productos
            SET nombre=%s,
                codigo=%s,
                categoria=%s,
                costo=%s,
                precio_venta=%s,
                stock=%s,
                descripcion=%s,
                estado=%s
            WHERE id_producto=%s
            AND id_empresa=%s
        """, (
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion,
            estado,
            id_producto,
            id_empresa
        ))

        connection.commit()

        return True, "Producto actualizado correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible actualizar el producto."

    finally:

        cursor.close()
        connection.close()


# ==========================
# ACTIVAR PRODUCTO
# ==========================

def activarProducto(id_empresa, id_producto):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE productos
            SET estado=1
            WHERE id_producto=%s
            AND id_empresa=%s
        """, (id_producto, id_empresa))

        connection.commit()

        return True, "Producto activado correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible activar el producto."

    finally:

        cursor.close()
        connection.close()


# ==========================
# DESACTIVAR PRODUCTO
# ==========================

def desactivarProducto(id_empresa, id_producto):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE productos
            SET estado=0
            WHERE id_producto=%s
            AND id_empresa=%s
        """, (id_producto, id_empresa))

        connection.commit()

        return True, "Producto desactivado correctamente."

    except mysql.Error as err:

        print(err)

        return False, "No fue posible desactivar el producto."

    finally:

        cursor.close()
        connection.close()


# ==========================
# CATEGORÍAS
# ==========================

def categorias(id_empresa):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar.", []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT DISTINCT categoria
            FROM productos
            WHERE id_empresa=%s
            ORDER BY categoria
        """, (id_empresa,))

        categorias = cursor.fetchall()

        return True, "Categorías obtenidas correctamente.", categorias

    except mysql.Error as err:

        print(err)

        return False, "No fue posible obtener las categorías.", []

    finally:

        cursor.close()
        connection.close()

# ==========================
# BUSCAR PRODUCTOS
# ==========================

def buscarProducto(id_empresa, texto="", filtro="todos"):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos.", []

    cursor = connection.cursor(dictionary=True)

    texto = f"%{texto}%"

    try:

        if filtro == "codigo":

            sql = """
                SELECT *
                FROM productos
                WHERE id_empresa=%s
                AND codigo LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (id_empresa, texto))

        elif filtro == "nombre":

            sql = """
                SELECT *
                FROM productos
                WHERE id_empresa=%s
                AND nombre LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (id_empresa, texto))

        elif filtro == "categoria":

            sql = """
                SELECT *
                FROM productos
                WHERE id_empresa=%s
                AND categoria LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (id_empresa, texto))

        else:

            sql = """
                SELECT *
                FROM productos
                WHERE id_empresa=%s
                AND (
                    codigo LIKE %s
                    OR nombre LIKE %s
                    OR categoria LIKE %s
                )
                ORDER BY nombre
            """

            cursor.execute(sql, (
                id_empresa,
                texto,
                texto,
                texto
            ))

        productos = cursor.fetchall()

        return True, "Productos encontrados.", productos

    except mysql.Error as err:

        print(err)

        return False, "No fue posible realizar la búsqueda.", []

    finally:

        cursor.close()
        connection.close()

