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

def registrarProducto(nombre, codigo, categoria, costo, precio_venta, stock, descripcion):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_producto
        FROM productos
        WHERE nombre=%s
        OR codigo=%s
    """, (nombre, codigo))

    if cursor.fetchone():
        cursor.close()
        connection.close()
        return False, "El nombre o el código del producto ya existen."

    cursor.close()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO productos
            (nombre,codigo,categoria,costo,precio_venta,stock,descripcion)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
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

def obtenerProducto(id_producto=None):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos.", None

    cursor = connection.cursor(dictionary=True)

    try:

        if id_producto is None:

            cursor.execute("""
                SELECT *
                FROM productos
                ORDER BY nombre
            """)

            productos = cursor.fetchall()

            return True, "Productos obtenidos correctamente.", productos

        cursor.execute("""
            SELECT *
            FROM productos
            WHERE id_producto=%s
        """, (id_producto,))

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
        WHERE (nombre=%s OR codigo=%s)
        AND id_producto<>%s
    """, (
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
        """, (
            nombre,
            codigo,
            categoria,
            costo,
            precio_venta,
            stock,
            descripcion,
            estado,
            id_producto
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

def activarProducto(id_producto):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE productos
            SET estado=1
            WHERE id_producto=%s
        """, (id_producto,))

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

def desactivarProducto(id_producto):

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE productos
            SET estado=0
            WHERE id_producto=%s
        """, (id_producto,))

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

def categorias():

    connection = connect()

    if connection is None:
        return False, "No fue posible conectar.", []

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT DISTINCT categoria
            FROM productos
            ORDER BY categoria
        """)

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

def buscarProducto(texto="", filtro="todos"):

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
                WHERE codigo LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (texto,))

        elif filtro == "nombre":

            sql = """
                SELECT *
                FROM productos
                WHERE nombre LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (texto,))

        elif filtro == "categoria":

            sql = """
                SELECT *
                FROM productos
                WHERE categoria LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (texto,))

        else:

            sql = """
                SELECT *
                FROM productos
                WHERE
                    codigo LIKE %s
                    OR nombre LIKE %s
                    OR categoria LIKE %s
                ORDER BY nombre
            """

            cursor.execute(sql, (
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

