from flask import session
import mysql.connector as mysql
from config import DB_CONFIG
from werkzeug.security import generate_password_hash,check_password_hash

def connect():
    try:
        connection=mysql.connect(**DB_CONFIG)
        print("Connected to the database successfully!")
        return connection
    except mysql.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def registrarUsuario(id_empresa,usuario,correo,password,rol):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT id_usuario
    FROM usuarios
    WHERE id_empresa=%s AND nombre_usuario=%s
    OR id_empresa=%s AND correo=%s
    """

    cursor.execute(sql,(id_empresa,usuario,id_empresa,correo))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False,"El nombre de usuario o el correo ya existen."

    cursor.close()

    cursor=connection.cursor()

    passwordHash=generate_password_hash(password)

    sql="""
    INSERT INTO usuarios(id_empresa,nombre_usuario,correo,password,rol)
    VALUES(%s,%s,%s,%s,%s)
    """

    try:

        cursor.execute(sql,(id_empresa,usuario,correo,passwordHash,rol))

        connection.commit()

        return True,"Usuario registrado correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible registrar el usuario."

    finally:

        cursor.close()
        connection.close()

def validarLogin(usuario,password):

    connection=connect()

    if connection is None:
        return None

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT *
    FROM usuarios
    WHERE nombre_usuario=%s
    AND estado=1
    """

    cursor.execute(sql,(usuario,))

    usuarioDB=cursor.fetchone()

    cursor.close()
    connection.close()

    if usuarioDB and check_password_hash(usuarioDB["password"],password):
        return usuarioDB

    return None

def buscarUsuario(usuario):

    connection=connect()

    if connection is None:
        return None

    cursor=connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=%s",(usuario,))

    resultado=cursor.fetchone()

    cursor.close()
    connection.close()

    return resultado

def obtenerUsuarios():

    connection=connect()

    if connection is None:
        return []

    cursor=connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios where id_empresa=%s ORDER BY fecha_creacion DESC",(session["id_empresa"],))

    usuarios=cursor.fetchall()

    cursor.close()
    connection.close()

    return usuarios

def obtenerUsuarioID(idUsuario):

    connection=connect()

    if connection is None:
        return None

    cursor=connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s AND id_empresa=%s",(idUsuario,session["id_empresa"]))

    usuario=cursor.fetchone()

    cursor.close()
    connection.close()

    return usuario

def actualizarUsuario(idUsuario,usuario,correo,rol,estado):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor(dictionary=True)

    sql="""
    SELECT id_usuario
    FROM usuarios
    WHERE (nombre_usuario=%s OR correo=%s)
    AND id_usuario<>%s
    """

    cursor.execute(sql,(usuario,correo,idUsuario))

    if cursor.fetchone():

        cursor.close()
        connection.close()

        return False,"El nombre de usuario o el correo ya están registrados."

    cursor.close()

    cursor=connection.cursor()

    sql="""
    UPDATE usuarios
    SET nombre_usuario=%s,
        correo=%s,
        rol=%s,
        estado=%s
    WHERE id_usuario=%s
    AND id_empresa=%s
    """

    try:

        cursor.execute(sql,(usuario,correo,rol,estado,idUsuario,session["id_empresa"]))

        connection.commit()

        return True,"Usuario actualizado correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible actualizar el usuario."

    finally:

        cursor.close()
        connection.close()

def cambiarPassword(idUsuario,password):

    connection=connect()

    if connection is None:
        return False,"No fue posible conectar con la base de datos."

    cursor=connection.cursor()

    passwordHash=generate_password_hash(password)

    sql="""
    UPDATE usuarios
    SET password=%s
    WHERE id_usuario=%s
    """

    try:

        cursor.execute(sql,(passwordHash,idUsuario))

        connection.commit()

        return True,"Contraseña actualizada correctamente."

    except mysql.Error as err:

        print(err)

        return False,"No fue posible actualizar la contraseña."

    finally:

        cursor.close()
        connection.close()

def activarUsuario(idUsuario):

    connection=connect()

    if connection is None:
        return False, "no fue posible conectar con la base de datos."

    cursor=connection.cursor()

    sql="""
    UPDATE usuarios
    SET estado=1
    WHERE id_usuario=%s
    """

    try:

        cursor.execute(sql,(idUsuario,))

        connection.commit()

        return True, "Usuario activado correctamente."

    except mysql.Error as err:

        print(err)

        return False, "no fue posible activar el usuario."

    finally:

        cursor.close()
        connection.close()

def desactivarUsuario(idUsuario):

    connection=connect()

    if connection is None:
        return False, "no fue posible conectar con la base de datos."

    cursor=connection.cursor()

    sql="""
    UPDATE usuarios
    SET estado=0
    WHERE id_usuario=%s
    """

    try:

        cursor.execute(sql,(idUsuario,))

        connection.commit()

        return True, "Usuario desactivado correctamente."

    except mysql.Error as err:

        print(err)

        return False, "no fue posible desactivar el usuario."

    finally:

        cursor.close()
        connection.close()