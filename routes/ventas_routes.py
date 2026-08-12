from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    send_file,
    abort
)

from auth import login_required

from models.ventas import (
    buscarProductoVenta,
    registrarVenta,
    obtenerVentaFactura
)

from utils.factura_pdf import (
    generarFacturaPDF
)


ventas_bp = Blueprint(
    "ventas",
    __name__
)


# ======================================
# VISTA PRINCIPAL
# ======================================

@ventas_bp.route("/ventas")
@login_required
def ventas():

    return render_template(
        "ventas/ventas.html"
    )


# ======================================
# BUSCAR PRODUCTOS
# ======================================

@ventas_bp.route("/buscar_producto")
@login_required
def buscar_producto():

    texto = request.args.get(
        "q",
        ""
    ).strip()


    if texto == "":

        return jsonify([])


    id_empresa = session.get(
        "id_empresa"
    )


    if not id_empresa:

        return jsonify([])


    ok, mensaje, productos = buscarProductoVenta(

        texto,

        id_empresa

    )


    if ok:

        return jsonify(productos)


    return jsonify([])


# ======================================
# REGISTRAR VENTA
# ======================================

@ventas_bp.route(
    "/registrar_venta",
    methods=["POST"]
)
@login_required
def registrar_venta():

    data = request.get_json()


    # ======================================
    # VALIDAR DATOS
    # ======================================

    if not data:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se recibieron datos."

        }), 400


    # ======================================
    # SESIÓN
    # ======================================

    id_usuario = session.get(
        "id_usuario"
    )

    id_empresa = session.get(
        "id_empresa"
    )


    if not id_usuario:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se encontró el usuario en sesión."

        }), 401


    if not id_empresa:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se encontró la empresa del usuario en sesión."

        }), 400


    # ======================================
    # VALIDAR PRODUCTOS
    # ======================================

    productos = data.get(
        "productos",
        []
    )


    if not productos:

        return jsonify({

            "ok": False,

            "mensaje":
                "La venta no contiene productos."

        }), 400


    try:

        # ==================================
        # REGISTRAR VENTA
        # ==================================

        ok, mensaje, id_venta = registrarVenta(

            id_empresa,

            id_usuario,

            data.get(
                "cliente",
                ""
            ),

            data.get(
                "documento",
                ""
            ),

            data.get(
                "fecha"
            ),

            data.get(
                "metodo_pago"
            ),

            data.get(
                "subtotal",
                0
            ),

            data.get(
                "descuento",
                0
            ),

            data.get(
                "iva",
                0
            ),

            data.get(
                "total",
                0
            ),

            data.get(
                "observaciones",
                ""
            ),

            productos

        )


        # ==================================
        # ERROR
        # ==================================

        if not ok:

            return jsonify({

                "ok": False,

                "mensaje": mensaje

            }), 400


        # ==================================
        # RESPUESTA EXITOSA
        # ==================================

        return jsonify({

            "ok": True,

            "mensaje": mensaje,

            "id_venta": id_venta,

            "factura_url": (
                f"/ventas/factura/{id_venta}"
            )

        })


    except Exception as err:

        print(
            "ERROR EN ROUTE registrar_venta:",
            err
        )


        return jsonify({

            "ok": False,

            "mensaje":
                "Ocurrió un error al registrar la venta."

        }), 500


# ======================================
# GENERAR FACTURA PDF
# ======================================

@ventas_bp.route(
    "/ventas/factura/<int:id_venta>"
)
@login_required
def factura(id_venta):

    # ======================================
    # EMPRESA DEL USUARIO
    # ======================================

    id_empresa = session.get(
        "id_empresa"
    )


    if not id_empresa:

        return jsonify({

            "ok": False,

            "mensaje":
                "No se encontró la empresa asociada."

        }), 400


    # ======================================
    # OBTENER VENTA
    # ======================================

    venta, productos = obtenerVentaFactura(

        id_empresa,

        id_venta

    )


    if venta is None:

        abort(404)


    # ======================================
    # GENERAR PDF
    # ======================================

    try:

        pdf = generarFacturaPDF(

            venta,

            productos

        )


        # ==================================
        # ENVIAR PDF AL NAVEGADOR
        # ==================================

        return send_file(

            pdf,

            mimetype="application/pdf",

            as_attachment=False,

            download_name=(
                f"factura_{id_venta}.pdf"
            )

        )


    except Exception as err:

        print(
            "ERROR AL GENERAR FACTURA:",
            err
        )


        return jsonify({

            "ok": False,

            "mensaje":
                "No fue posible generar la factura."

        }), 500