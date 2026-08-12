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
# REGISTRAR INGRESO
# =====================================================

def registrarIngreso(
    id_empresa,
    id_usuario,
    concepto,
    monto,
    categoria,
    fecha,
    descripcion
):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO ingresos
            (
                id_empresa,
                id_usuario,
                concepto,
                monto,
                categoria,
                fecha,
                descripcion
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            id_empresa,
            id_usuario,
            concepto,
            monto,
            categoria,
            fecha,
            descripcion
        ))

        connection.commit()

        return True, "Ingreso registrado correctamente."

    except mysql.Error as err:

        connection.rollback()

        print("Error al registrar ingreso:", err)

        return False, str(err)

    finally:

        cursor.close()
        connection.close()


# =====================================================
# REGISTRAR GASTO
# =====================================================

def registrarGasto(
    id_empresa,
    id_usuario,
    concepto,
    categoria,
    monto,
    fecha,
    descripcion
):

    connection = connect()

    if connection is None:

        return False, "No fue posible conectar con la base de datos."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO gastos
            (
                id_empresa,
                id_usuario,
                concepto,
                categoria,
                monto,
                fecha,
                descripcion
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            id_empresa,
            id_usuario,
            concepto,
            categoria,
            monto,
            fecha,
            descripcion
        ))

        connection.commit()

        return True, "Gasto registrado correctamente."

    except mysql.Error as err:

        connection.rollback()

        print("Error al registrar gasto:", err)

        return False, str(err)

    finally:

        cursor.close()
        connection.close()



# =====================================================
# RESUMEN DE FINANZAS
# =====================================================

def resumenFinanzas(id_empresa):

    connection = connect()

    if connection is None:

        return {
            "ingresos_dia": 0,
            "gastos_dia": 0,
            "utilidad": 0,
            "saldo_caja": 0
        }

    cursor = connection.cursor(dictionary=True)

    try:

        # =============================================
        # FECHA ACTUAL DE MYSQL
        # =============================================

        cursor.execute("""
            SELECT CURDATE() AS hoy
        """)

        hoy = cursor.fetchone()["hoy"]

        print("FECHA MYSQL:", hoy)
        print("ID EMPRESA:", id_empresa)


        # =============================================
        # INGRESOS DEL DÍA
        # =============================================

        cursor.execute("""
        SELECT
            COALESCE(SUM(monto), 0) AS ingresos_dia
        FROM ingresos
        WHERE id_empresa = %s
        AND DATE(created_at) = CURDATE()
    """, (
        id_empresa,
    ))

        ingresos_dia = cursor.fetchone()["ingresos_dia"]


        # =============================================
        # GASTOS DEL DÍA
        # =============================================

        cursor.execute("""
        SELECT
            COALESCE(SUM(monto), 0) AS gastos_dia
        FROM gastos
        WHERE id_empresa = %s
        AND DATE(created_at) = CURDATE()
    """, (
        id_empresa,
    ))

        gastos_dia = cursor.fetchone()["gastos_dia"]


        # =============================================
        # UTILIDAD
        # =============================================

        utilidad = (
            ingresos_dia - gastos_dia
        )


        # =============================================
        # SALDO
        # =============================================

        saldo_caja = utilidad


        print("INGRESOS DEL DÍA:", ingresos_dia)
        print("GASTOS DEL DÍA:", gastos_dia)
        print("UTILIDAD:", utilidad)


        return {

            "ingresos_dia": ingresos_dia,
            "gastos_dia": gastos_dia,
            "utilidad": utilidad,
            "saldo_caja": saldo_caja

        }


    except mysql.Error as err:

        print(
            "ERROR REAL EN resumenFinanzas:",
            err
        )

        return {

            "ingresos_dia": 0,
            "gastos_dia": 0,
            "utilidad": 0,
            "saldo_caja": 0

        }

    finally:

        cursor.close()
        connection.close()


# =====================================================
# BALANCE GENERAL
# =====================================================

def obtenerBalanceGeneral(id_empresa):

    connection = connect()

    if connection is None:

        return {

            "total_ingresos": 0,

            "total_gastos": 0,

            "cuentas_cobrar": 0,

            "cuentas_pagar": 0,

            "utilidad_neta": 0

        }

    cursor = connection.cursor(dictionary=True)

    try:

        # =============================================
        # TOTAL INGRESOS
        # =============================================

        cursor.execute("""
            SELECT
                COALESCE(SUM(monto), 0) AS total_ingresos

            FROM ingresos

            WHERE id_empresa = %s
        """, (
            id_empresa,
        ))

        total_ingresos = cursor.fetchone()[
            "total_ingresos"
        ]


        # =============================================
        # TOTAL GASTOS
        # =============================================

        cursor.execute("""
            SELECT
                COALESCE(SUM(monto), 0) AS total_gastos

            FROM gastos

            WHERE id_empresa = %s
        """, (
            id_empresa,
        ))

        total_gastos = cursor.fetchone()[
            "total_gastos"
        ]


        # =============================================
        # UTILIDAD NETA
        # =============================================

        utilidad_neta = (
            total_ingresos
            - total_gastos
        )


        return {

            "total_ingresos":
                total_ingresos,

            "total_gastos":
                total_gastos,

            "cuentas_cobrar":
                0,

            "cuentas_pagar":
                0,

            "utilidad_neta":
                utilidad_neta

        }


    except mysql.Error as err:

        print(
            "Error en obtenerBalanceGeneral:",
            err
        )

        return {

            "total_ingresos": 0,

            "total_gastos": 0,

            "cuentas_cobrar": 0,

            "cuentas_pagar": 0,

            "utilidad_neta": 0

        }

    finally:

        cursor.close()
        connection.close()


# =====================================================
# OBTENER INGRESOS
# =====================================================

def obtenerIngresos(id_empresa):

    connection = connect()

    if connection is None:

        return False, []


    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                id_ingreso,

                id_usuario,

                concepto,

                monto,

                categoria,

                fecha,

                descripcion

            FROM ingresos

            WHERE id_empresa = %s

            ORDER BY
                fecha DESC,
                id_ingreso DESC

        """, (
            id_empresa,
        ))


        ingresos = cursor.fetchall()


        return True, ingresos


    except mysql.Error as err:

        print(
            "Error al consultar ingresos:",
            err
        )

        return False, []


    finally:

        cursor.close()
        connection.close()


# =====================================================
# OBTENER GASTOS
# =====================================================

def obtenerGastos(id_empresa):

    connection = connect()

    if connection is None:

        return False, []


    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                id_gasto,

                id_usuario,

                concepto,

                categoria,

                monto,

                fecha,

                descripcion

            FROM gastos

            WHERE id_empresa = %s

            ORDER BY
                fecha DESC,
                id_gasto DESC

        """, (
            id_empresa,
        ))


        gastos = cursor.fetchall()


        return True, gastos


    except mysql.Error as err:

        print(
            "Error al consultar gastos:",
            err
        )

        return False, []


    finally:

        cursor.close()
        connection.close()