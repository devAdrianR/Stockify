from io import BytesIO
from decimal import Decimal
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# =====================================================
# FORMATEAR MONEDA
# =====================================================

def formatear_moneda(valor):

    if valor is None:
        valor = 0

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        valor = 0

    return "${:,.0f}".format(valor)


# =====================================================
# FORMATEAR FECHA
# =====================================================

def formatear_fecha(fecha):

    if not fecha:
        return "-"

    if isinstance(fecha, datetime):

        return fecha.strftime(
            "%d/%m/%Y %H:%M"
        )

    return str(fecha)


# =====================================================
# GENERAR FACTURA PDF
# =====================================================

def generarFacturaPDF(venta, productos):

    buffer = BytesIO()


    # =================================================
    # DOCUMENTO
    # =================================================

    documento = SimpleDocTemplate(

        buffer,

        pagesize=LETTER,

        rightMargin=15 * mm,

        leftMargin=15 * mm,

        topMargin=15 * mm,

        bottomMargin=15 * mm

    )


    # =================================================
    # ESTILOS
    # =================================================

    estilos = getSampleStyleSheet()


    titulo = ParagraphStyle(

        "Titulo",

        parent=estilos["Heading1"],

        fontName="Helvetica-Bold",

        fontSize=20,

        leading=24,

        alignment=TA_CENTER,

        spaceAfter=8

    )


    subtitulo = ParagraphStyle(

        "Subtitulo",

        parent=estilos["Normal"],

        fontName="Helvetica",

        fontSize=9,

        leading=12,

        alignment=TA_CENTER,

        textColor=colors.HexColor(
            "#666666"
        ),

        spaceAfter=15

    )


    normal = ParagraphStyle(

        "NormalFactura",

        parent=estilos["Normal"],

        fontName="Helvetica",

        fontSize=9,

        leading=12

    )


    pequeno = ParagraphStyle(

        "Pequeno",

        parent=estilos["Normal"],

        fontName="Helvetica",

        fontSize=8,

        leading=10

    )


    derecha = ParagraphStyle(

        "Derecha",

        parent=normal,

        alignment=TA_RIGHT

    )


    centro = ParagraphStyle(

        "Centro",

        parent=normal,

        alignment=TA_CENTER

    )


    # =================================================
    # CONTENIDO
    # =================================================

    elementos = []


    # =================================================
    # ENCABEZADO
    # =================================================

    elementos.append(
        Paragraph(
            "STOCKIFY",
            titulo
        )
    )


    elementos.append(
        Paragraph(
            "Factura de venta",
            subtitulo
        )
    )


    # =================================================
    # INFORMACIÓN DE LA FACTURA
    # =================================================

    informacion = [

        [
            Paragraph(
                "<b>Factura No.</b>",
                normal
            ),

            Paragraph(
                f"#{venta['id_venta']}",
                normal
            ),

            Paragraph(
                "<b>Fecha</b>",
                normal
            ),

            Paragraph(
                formatear_fecha(
                    venta["fecha"]
                ),
                normal
            )
        ],

        [
            Paragraph(
                "<b>Cliente</b>",
                normal
            ),

            Paragraph(
                str(
                    venta.get(
                        "cliente",
                        "-"
                    )
                ),
                normal
            ),

            Paragraph(
                "<b>Documento</b>",
                normal
            ),

            Paragraph(
                str(
                    venta.get(
                        "documento",
                        "-"
                    ) or "-"
                ),
                normal
            )
        ],

        [
            Paragraph(
                "<b>Método de pago</b>",
                normal
            ),

            Paragraph(
                str(
                    venta.get(
                        "metodo_pago",
                        "-"
                    )
                ),
                normal
            ),

            Paragraph(
                "<b>Estado</b>",
                normal
            ),

            Paragraph(
                str(
                    venta.get(
                        "estado",
                        "-"
                    )
                ),
                normal
            )
        ]

    ]


    tabla_informacion = Table(

        informacion,

        colWidths=[
            28 * mm,
            60 * mm,
            28 * mm,
            65 * mm
        ]

    )


    tabla_informacion.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#F4F8F6")
            ),

            (
                "BACKGROUND",
                (2, 0),
                (2, -1),
                colors.HexColor("#F4F8F6")
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.6,
                colors.HexColor("#DCE6E1")
            ),

            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#DCE6E1")
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])

    )


    elementos.append(
        tabla_informacion
    )

    elementos.append(
        Spacer(1, 8 * mm)
    )


    # =================================================
    # TABLA DE PRODUCTOS
    # =================================================

    datos_productos = [

        [
            Paragraph(
                "<b>Código</b>",
                centro
            ),

            Paragraph(
                "<b>Producto</b>",
                centro
            ),

            Paragraph(
                "<b>Cant.</b>",
                centro
            ),

            Paragraph(
                "<b>Precio</b>",
                centro
            ),

            Paragraph(
                "<b>Subtotal</b>",
                centro
            )

        ]

    ]


    for producto in productos:

        datos_productos.append([

            Paragraph(
                str(
                    producto.get(
                        "codigo",
                        "-"
                    )
                ),
                centro
            ),

            Paragraph(
                str(
                    producto.get(
                        "nombre",
                        "-"
                    )
                ),
                normal
            ),

            Paragraph(
                str(
                    producto.get(
                        "cantidad",
                        0
                    )
                ),
                centro
            ),

            Paragraph(
                formatear_moneda(
                    producto.get(
                        "precio",
                        0
                    )
                ),
                derecha
            ),

            Paragraph(
                formatear_moneda(
                    producto.get(
                        "subtotal",
                        0
                    )
                ),
                derecha
            )

        ])


    tabla_productos = Table(

        datos_productos,

        colWidths=[
            27 * mm,
            72 * mm,
            20 * mm,
            32 * mm,
            35 * mm
        ],

        repeatRows=1

    )


    tabla_productos.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#2D6A4F")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#DCE6E1")
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#F8FBF9")
                ]
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])

    )


    elementos.append(
        tabla_productos
    )


    elementos.append(
        Spacer(1, 8 * mm)
    )


    # =================================================
    # TOTALES
    # =================================================

    subtotal = venta.get(
        "subtotal",
        0
    )

    descuento = venta.get(
        "descuento",
        0
    )

    iva = venta.get(
        "iva",
        0
    )

    total = venta.get(
        "total",
        0
    )


    tabla_totales = Table(

        [

            [
                Paragraph(
                    "<b>Subtotal</b>",
                    normal
                ),

                Paragraph(
                    formatear_moneda(
                        subtotal
                    ),
                    derecha
                )
            ],

            [
                Paragraph(
                    "Descuento",
                    normal
                ),

                Paragraph(
                    formatear_moneda(
                        descuento
                    ),
                    derecha
                )
            ],

            [
                Paragraph(
                    "IVA",
                    normal
                ),

                Paragraph(
                    formatear_moneda(
                        iva
                    ),
                    derecha
                )
            ],

            [
                Paragraph(
                    "<b>TOTAL</b>",
                    normal
                ),

                Paragraph(
                    f"<b>{formatear_moneda(total)}</b>",
                    derecha
                )
            ]

        ],

        colWidths=[
            45 * mm,
            40 * mm
        ]

    )


    tabla_totales.setStyle(

        TableStyle([

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "RIGHT"
            ),

            (
                "LINEBELOW",
                (0, 0),
                (-1, 2),
                0.5,
                colors.HexColor("#DCE6E1")
            ),

            (
                "BACKGROUND",
                (0, 3),
                (-1, 3),
                colors.HexColor("#F4F8F6")
            ),

            (
                "TEXTCOLOR",
                (1, 3),
                (1, 3),
                colors.HexColor("#2D6A4F")
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )

        ])

    )


    # Alinear los totales a la derecha
    tabla_totales.hAlign = "RIGHT"


    elementos.append(
        tabla_totales
    )


    # =================================================
    # OBSERVACIONES
    # =================================================

    observaciones = venta.get(
        "observaciones"
    )


    if observaciones:

        elementos.append(
            Spacer(1, 6 * mm)
        )


        elementos.append(
            Paragraph(
                "<b>Observaciones</b>",
                normal
            )
        )


        elementos.append(
            Spacer(1, 2 * mm)
        )


        elementos.append(
            Paragraph(
                str(observaciones),
                pequeno
            )
        )


    # =================================================
    # PIE DE FACTURA
    # =================================================

    elementos.append(
        Spacer(1, 10 * mm)
    )


    elementos.append(
        Paragraph(
            "Gracias por su compra.",
            subtitulo
        )
    )


    # =================================================
    # CONSTRUIR PDF
    # =================================================

    documento.build(
        elementos
    )


    buffer.seek(0)

    return buffer