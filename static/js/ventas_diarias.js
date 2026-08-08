/* =========================================================
   VENTAS DIARIAS - JAVASCRIPT
   Stockify
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       ELEMENTOS
    ===================================================== */

    const modal = document.getElementById("modalDetalle");
    const cerrarModal = document.getElementById("cerrarModal");
    const detalleVenta = document.getElementById("detalleVenta");

    const botonesDetalle = document.querySelectorAll(".btn-detail");


    /* =====================================================
       COMPROBAR ELEMENTOS
    ===================================================== */

    console.log("Ventas diarias cargado.");
    console.log("Botones de detalle:", botonesDetalle.length);


    /* =====================================================
       ABRIR DETALLE DE VENTA
    ===================================================== */

    botonesDetalle.forEach(function (boton) {

        boton.addEventListener("click", function () {

            const idVenta = this.dataset.id;

            console.log("Consultando venta:", idVenta);

            if (!idVenta) {

                console.error("No se encontró el ID de la venta.");

                return;

            }

            abrirDetalle(idVenta);

        });

    });


    /* =====================================================
       FUNCIÓN ABRIR DETALLE
    ===================================================== */

    function abrirDetalle(idVenta) {

        /* Abrir modal */

        modal.classList.add("active");


        /* Mostrar cargando */

        detalleVenta.innerHTML = `

            <div class="loading">

                <i class="fa-solid fa-spinner fa-spin"></i>

                <p>
                    Cargando información de la venta...
                </p>

            </div>

        `;


        /* =================================================
           CONSULTAR FLASK
        ================================================= */

        fetch(`/reportes/detalle_venta/${idVenta}`)

            .then(function (response) {

                if (!response.ok) {

                    throw new Error(
                        "Error HTTP: " + response.status
                    );

                }

                return response.json();

            })

            .then(function (data) {

                console.log("Respuesta detalle:", data);


                if (!data.ok) {

                    mostrarError(
                        data.mensaje ||
                        "No fue posible obtener la venta."
                    );

                    return;

                }


                mostrarDetalle(
                    data.venta,
                    data.productos
                );

            })

            .catch(function (error) {

                console.error(
                    "Error obteniendo detalle:",
                    error
                );

                mostrarError(
                    "No fue posible cargar el detalle de la venta."
                );

            });

    }


    /* =====================================================
       MOSTRAR DETALLE
    ===================================================== */

    function mostrarDetalle(venta, productos) {

        if (!venta) {

            mostrarError(
                "La información de la venta está vacía."
            );

            return;

        }


        if (!productos) {

            productos = [];

        }


        /* =================================================
           FORMATEAR VALORES
        ================================================= */

        const subtotal = numero(venta.subtotal);

        const descuento = numero(venta.descuento);

        const iva = numero(venta.iva);

        const total = numero(venta.total);


        /* =================================================
           FECHA
        ================================================= */

        const fecha = formatearFecha(venta.fecha);


        /* =================================================
           PRODUCTOS
        ================================================= */

        let filasProductos = "";


        if (productos.length > 0) {

            productos.forEach(function (producto) {

                filasProductos += `

                    <tr>

                        <td>
                            ${escapeHTML(
                                producto.codigo || "-"
                            )}
                        </td>

                        <td>
                            ${escapeHTML(
                                producto.nombre || "-"
                            )}
                        </td>

                        <td>
                            ${producto.cantidad || 0}
                        </td>

                        <td>
                            ${formatearMoneda(
                                producto.precio
                            )}
                        </td>

                        <td>
                            ${formatearMoneda(
                                producto.subtotal
                            )}
                        </td>

                    </tr>

                `;

            });

        } else {

            filasProductos = `

                <tr>

                    <td
                        colspan="5"
                        class="empty">

                        No hay productos asociados
                        a esta venta.

                    </td>

                </tr>

            `;

        }


        /* =================================================
           HTML DEL DETALLE
        ================================================= */

        detalleVenta.innerHTML = `

            <div class="detail-container">


                <!-- =====================================
                     INFORMACIÓN GENERAL
                ====================================== -->

                <div class="detail-section">

                    <h3>

                        <i class="fa-solid fa-circle-info"></i>

                        Información de la venta

                    </h3>


                    <div class="detail-grid">


                        <div class="detail-item">

                            <span>
                                Número de venta
                            </span>

                            <strong>
                                #${venta.id_venta}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Fecha
                            </span>

                            <strong>
                                ${fecha}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Cliente
                            </span>

                            <strong>
                                ${escapeHTML(
                                    venta.cliente || "-"
                                )}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Documento
                            </span>

                            <strong>
                                ${escapeHTML(
                                    venta.documento || "-"
                                )}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Método de pago
                            </span>

                            <strong>
                                ${escapeHTML(
                                    venta.metodo_pago || "-"
                                )}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Usuario
                            </span>

                            <strong>
                                ${escapeHTML(
                                    venta.nombre_usuario || "-"
                                )}
                            </strong>

                        </div>


                    </div>

                </div>



                <!-- =====================================
                     PRODUCTOS
                ====================================== -->

                <div class="detail-section">

                    <h3>

                        <i class="fa-solid fa-boxes-stacked"></i>

                        Productos vendidos

                    </h3>


                    <div class="detail-table-container">

                        <table class="detail-table">


                            <thead>

                                <tr>

                                    <th>
                                        Código
                                    </th>

                                    <th>
                                        Producto
                                    </th>

                                    <th>
                                        Cantidad
                                    </th>

                                    <th>
                                        Precio
                                    </th>

                                    <th>
                                        Subtotal
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                ${filasProductos}

                            </tbody>


                        </table>

                    </div>

                </div>



                <!-- =====================================
                     TOTALES
                ====================================== -->

                <div class="detail-section totals-section">

                    <h3>

                        <i class="fa-solid fa-calculator"></i>

                        Resumen de pago

                    </h3>


                    <div class="totals">


                        <div class="total-row">

                            <span>
                                Subtotal
                            </span>

                            <strong>
                                ${formatearMoneda(subtotal)}
                            </strong>

                        </div>


                        <div class="total-row">

                            <span>
                                Descuento
                            </span>

                            <strong class="discount">

                                - ${formatearMoneda(descuento)}

                            </strong>

                        </div>


                        <div class="total-row">

                            <span>
                                IVA
                            </span>

                            <strong>
                                ${formatearMoneda(iva)}
                            </strong>

                        </div>


                        <div class="total-row total-final">

                            <span>
                                Total
                            </span>

                            <strong>
                                ${formatearMoneda(total)}
                            </strong>

                        </div>


                    </div>

                </div>



                <!-- =====================================
                     OBSERVACIONES
                ====================================== -->

                ${venta.observaciones ? `

                    <div class="detail-section">

                        <h3>

                            <i class="fa-solid fa-comment"></i>

                            Observaciones

                        </h3>


                        <div class="observaciones">

                            ${escapeHTML(
                                venta.observaciones
                            )}

                        </div>

                    </div>

                ` : ""}


            </div>

        `;

    }


    /* =====================================================
       MOSTRAR ERROR
    ===================================================== */

    function mostrarError(mensaje) {

        detalleVenta.innerHTML = `

            <div class="detail-error">

                <i class="fa-solid fa-circle-exclamation"></i>

                <h3>
                    Ocurrió un problema
                </h3>

                <p>
                    ${escapeHTML(mensaje)}
                </p>

            </div>

        `;

    }


    /* =====================================================
       CERRAR MODAL
    ===================================================== */

    cerrarModal.addEventListener("click", function () {

        cerrarDetalle();

    });


    /* =====================================================
       CERRAR AL HACER CLICK FUERA
    ===================================================== */

    modal.addEventListener("click", function (event) {

        if (event.target === modal) {

            cerrarDetalle();

        }

    });


    /* =====================================================
       CERRAR CON ESC
    ===================================================== */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            if (modal.classList.contains("active")) {

                cerrarDetalle();

            }

        }

    });


    /* =====================================================
       CERRAR DETALLE
    ===================================================== */

    function cerrarDetalle() {

        modal.classList.remove("active");

        detalleVenta.innerHTML = `

            <div class="loading">

                <i class="fa-solid fa-spinner fa-spin"></i>

                <p>
                    Cargando información...
                </p>

            </div>

        `;

    }


    /* =====================================================
       CONVERTIR A NÚMERO
    ===================================================== */

    function numero(valor) {

        if (
            valor === null ||
            valor === undefined ||
            valor === ""
        ) {

            return 0;

        }

        const resultado = Number(valor);

        return isNaN(resultado)
            ? 0
            : resultado;

    }


    /* =====================================================
       FORMATEAR MONEDA
    ===================================================== */

    function formatearMoneda(valor) {

        const numeroValor = numero(valor);

        return "$" + numeroValor.toLocaleString(
            "es-CO",
            {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }
        );

    }


    /* =====================================================
       FORMATEAR FECHA
    ===================================================== */

    function formatearFecha(fecha) {

        if (!fecha) {

            return "-";

        }


        try {

            const fechaJS = new Date(
                fecha.replace(" ", "T")
            );


            if (isNaN(fechaJS.getTime())) {

                return fecha;

            }


            return fechaJS.toLocaleString(
                "es-CO",
                {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit"
                }
            );

        } catch (error) {

            return fecha;

        }

    }


    /* =====================================================
       ESCAPAR HTML
       Evita insertar directamente contenido
       proveniente de la base de datos.
    ===================================================== */

    function escapeHTML(valor) {

        if (
            valor === null ||
            valor === undefined
        ) {

            return "";

        }


        return String(valor)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

    }


});