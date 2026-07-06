import mysql.connector as mysql
from config import DB_CONFIG

def connect():
    try:
        connection=mysql.connect(**DB_CONFIG)
        print("Connected to the database successfully!")
        return connection
    except mysql.Error as err:
        print(f"Error connecting to the database: {err}")
        return None
    
def registrarProducto(nombre,codigo,categoria,costo,precio_venta,stock,descripcion):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT id_producto
    FROM productos
    WHERE nombre=%s
    OR codigo=%s
    """

    cursor.execute(sql,(nombre,codigo))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False,"El nombre o el código del producto ya existen."

    cursor.close()

    cursor=connection.cursor()

    sql="""
    INSERT INTO productos(nombre,codigo,categoria,costo,precio_venta,stock,descripcion)
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    try:

        cursor.execute(sql,(nombre,codigo,categoria,costo,precio_venta,stock,descripcion))

        connection.commit()

        return True,"Producto registrado correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible registrar el producto."

    finally:

        cursor.close()
        connection.close()

def editarProducto(id_producto,nombre,codigo,categoria,costo,precio_venta,stock,descripcion):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT id_producto
    FROM productos
    WHERE (nombre=%s OR codigo=%s)
    AND id_producto!=%s
    """

    cursor.execute(sql,(nombre,codigo,id_producto))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False,"El nombre o el código del producto ya existen."

    cursor.close()

    cursor=connection.cursor()

    sql="""
    UPDATE productos
    SET nombre=%s,
        codigo=%s,
        categoria=%s,
        costo=%s,
        precio_venta=%s,
        stock=%s,
        descripcion=%s
    WHERE id_producto=%s
    """

    try:

        cursor.execute(sql,(nombre,codigo,categoria,costo,precio_venta,stock,descripcion,id_producto))

        connection.commit()

        return True,"Producto editado correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible editar el producto."

    finally:

        cursor.close()
        connection.close()

def eliminarProducto(id_producto):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor()

    sql="""
    DELETE FROM productos
    WHERE id_producto=%s
    """

    try:

        cursor.execute(sql,(id_producto,))

        connection.commit()

        return True,"Producto eliminado correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible eliminar el producto."

    finally:

        cursor.close()
        connection.close()

def verInventario():

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos.",[]

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT *
    FROM productos
    """

    try:

        cursor.execute(sql)

        productos=cursor.fetchall()

        return True,"Inventario obtenido correctamente.",productos

    except mysql.Error as err:

        print(err)

        return False,"No fue posible obtener el inventario.",[]

    finally:

        cursor.close()
        connection.close()

def categorias():

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos.",[]

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT DISTINCT categoria
    FROM productos
    """

    try:

        cursor.execute(sql)

        categorias=cursor.fetchall()

        return True,"Categorías obtenidas correctamente.",categorias

    except mysql.Error as err:

        print(err)

        return False,"No fue posible obtener las categorías.",[]

    finally:

        cursor.close()
        connection.close()

def movimientos():

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos.",[]

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT *
    FROM movimientos
    """

    try:

        cursor.execute(sql)

        movimientos=cursor.fetchall()

        return True,"Movimientos obtenidos correctamente.",movimientos

    except mysql.Error as err:

        print(err)

        return False,"No fue posible obtener los movimientos.",[]

    finally:

        cursor.close()
        connection.close()

