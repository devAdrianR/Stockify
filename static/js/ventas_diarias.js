/* =========================================================
   VENTAS DIARIAS - JAVASCRIPT
   Stockify
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("=================================");
    console.log("VENTAS_DIARIAS.JS CARGADO");
    console.log("=================================");


    /* =====================================================
       ELEMENTOS
    ===================================================== */

    const modal = document.getElementById("modalDetalle");
    const cerrarModal = document.getElementById("cerrarModal");
    const detalleVenta = document.getElementById("detalleVenta");

    const botonesDetalle =
        document.querySelectorAll(".btn-detail");


    console.log("Ventas diarias cargado.");
    console.log(
        "Botones de detalle:",
        botonesDetalle.length
    );


    /* =====================================================
       VERIFICAR ELEMENTOS
    ===================================================== */

    if (!modal) {

        console.error(
            "ERROR: No existe #modalDetalle"
        );

        return;
    }


    if (!cerrarModal) {

        console.error(
            "ERROR: No existe #cerrarModal"
        );

        return;
    }


    if (!detalleVenta) {

        console.error(
            "ERROR: No existe #detalleVenta"
        );

        return;
    }


    /* =====================================================
       BOTONES DE DETALLE
    ===================================================== */

    botonesDetalle.forEach(function (boton) {

        boton.addEventListener("click", function () {

            const idVenta = this.dataset.id;
            const urlDetalle = this.dataset.url;


            console.log("=================================");
            console.log("CLICK EN DETALLE");
            console.log("ID venta:", idVenta);
            console.log("URL detalle:", urlDetalle);
            console.log("=================================");


            if (!idVenta) {

                console.error(
                    "No se encontró el ID de la venta."
                );

                return;
            }


            if (!urlDetalle) {

                console.error(
                    "No se encontró la URL del detalle."
                );

                return;
            }


            abrirDetalle(
                idVenta,
                urlDetalle
            );

        });

    });


    /* =====================================================
       ABRIR DETALLE
    ===================================================== */

    function abrirDetalle(idVenta, urlDetalle) {

        console.log("=================================");
        console.log("ABRIENDO DETALLE");
        console.log("ID:", idVenta);
        console.log("URL:", urlDetalle);
        console.log("=================================");


        /* =================================================
           MOSTRAR MODAL

           IMPORTANTE:
           El CSS utiliza .modal.show
        ================================================= */

        modal.classList.add("show");


        console.log(
            "Modal:",
            modal
        );


        console.log(
            "Contenedor detalle:",
            detalleVenta
        );


        /* =================================================
           MOSTRAR CARGANDO
        ================================================= */

        detalleVenta.innerHTML = `

            <div class="loading">

                <i class="fa-solid fa-spinner fa-spin"></i>

                <p>
                    Cargando información de la venta...
                </p>

            </div>

        `;


        console.log(
            "Modal abierto. Ahora consultando Flask..."
        );


        /* =================================================
           CONSULTAR FLASK
        ================================================= */

        fetch(urlDetalle)

            .then(function (response) {

                console.log(
                    "Respuesta HTTP:",
                    response.status
                );


                if (!response.ok) {

                    throw new Error(
                        "Error HTTP: " +
                        response.status
                    );

                }


                return response.json();

            })


            .then(function (data) {

                console.log(
                    "Respuesta de Flask:",
                    data
                );


                if (!data.ok) {

                    mostrarError(
                        data.mensaje ||
                        "No fue posible obtener la venta."
                    );

                    return;

                }


                console.log(
                    "Venta recibida:",
                    data.venta
                );


                console.log(
                    "Productos recibidos:",
                    data.productos
                );


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

    function mostrarDetalle(
        venta,
        productos
    ) {


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
           DATOS
        ================================================= */

        const subtotal =
            numero(venta.subtotal);


        const descuento =
            numero(venta.descuento);


        const iva =
            numero(venta.iva);


        const total =
            numero(venta.total);


        const fecha =
            formatearFecha(venta.fecha);


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

                        <i class="fa-solid fa-circle-info"></i>

                        No hay productos asociados
                        a esta venta.

                    </td>

                </tr>

            `;

        }


        /* =================================================
           GENERAR HTML
        ================================================= */

        detalleVenta.innerHTML = `

            <div class="detail-container">


                <!-- =====================================
                     INFORMACIÓN DE LA VENTA
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
                                #${escapeHTML(
                                    venta.id_venta
                                )}
                            </strong>

                        </div>


                        <div class="detail-item">

                            <span>
                                Fecha
                            </span>

                            <strong>
                                ${escapeHTML(fecha)}
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
                     RESUMEN DE PAGO
                ====================================== -->

                <div class="detail-section">

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
                                ${formatearMoneda(
                                    subtotal
                                )}
                            </strong>

                        </div>


                        <div class="total-row">

                            <span>
                                Descuento
                            </span>

                            <strong class="discount">

                                - ${formatearMoneda(
                                    descuento
                                )}

                            </strong>

                        </div>


                        <div class="total-row">

                            <span>
                                IVA
                            </span>

                            <strong>
                                ${formatearMoneda(
                                    iva
                                )}
                            </strong>

                        </div>


                        <div class="total-row total-final">

                            <span>
                                Total
                            </span>

                            <strong>
                                ${formatearMoneda(
                                    total
                                )}
                            </strong>

                        </div>


                    </div>

                </div>



                <!-- =====================================
                     OBSERVACIONES
                ====================================== -->

                ${
                    venta.observaciones
                    ?
                    `

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

                    `
                    :
                    ""
                }


            </div>

        `;


        console.log(
            "Detalle de venta renderizado correctamente."
        );

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

    cerrarModal.addEventListener(
        "click",
        function () {

            cerrarDetalle();

        }
    );


    /* =====================================================
       CERRAR HACIENDO CLICK FUERA
    ===================================================== */

    modal.addEventListener(
        "click",
        function (event) {

            if (
                event.target === modal
            ) {

                cerrarDetalle();

            }

        }
    );


    /* =====================================================
       CERRAR CON ESC
    ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                modal.classList.contains("show")
            ) {

                cerrarDetalle();

            }

        }
    );


    /* =====================================================
       CERRAR DETALLE
    ===================================================== */

    function cerrarDetalle() {

        console.log(
            "Cerrando detalle..."
        );


        modal.classList.remove("show");


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


        const resultado =
            Number(valor);


        return isNaN(resultado)
            ? 0
            : resultado;

    }


    /* =====================================================
       FORMATEAR MONEDA
    ===================================================== */

    function formatearMoneda(valor) {

        const numeroValor =
            numero(valor);


        return "$" +
            numeroValor.toLocaleString(
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

            const fechaTexto =
                String(fecha);


            const fechaJS =
                new Date(
                    fechaTexto.replace(
                        " ",
                        "T"
                    )
                );


            if (
                isNaN(
                    fechaJS.getTime()
                )
            ) {

                return fechaTexto;

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

            return String(fecha);

        }

    }


    /* =====================================================
       ESCAPAR HTML
    ===================================================== */

    function escapeHTML(valor) {

        if (
            valor === null ||
            valor === undefined
        ) {

            return "";

        }


        return String(valor)
            .replace(
                /&/g,
                "&amp;"
            )
            .replace(
                /</g,
                "&lt;"
            )
            .replace(
                />/g,
                "&gt;"
            )
            .replace(
                /"/g,
                "&quot;"
            )
            .replace(
                /'/g,
                "&#039;"
            );

    }

});