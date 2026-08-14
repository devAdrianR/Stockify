console.log("Ventas JS cargado correctamente.");

let productosVenta = [];
let productoSeleccionado = null;


//=====================================
// ELEMENTOS
//=====================================

const inputBuscar =
    document.getElementById("buscar_producto");

const listaProductos =
    document.getElementById("lista_productos");

const idProducto =
    document.getElementById("id_producto");

const precio =
    document.getElementById("precio");

const cantidad =
    document.getElementById("cantidad");

const btnAgregar =
    document.getElementById("agregar_producto");

const detalleVenta =
    document.getElementById("detalle_venta");

const subtotalHTML =
    document.getElementById("subtotal");

const ivaHTML =
    document.getElementById("iva");

const descuentoHTML =
    document.getElementById("descuento");

const totalHTML =
    document.getElementById("total");

const totalProductosHTML =
    document.getElementById("total_productos");

const descuentoInput =
    document.getElementById("descuento_input");

const aplicarIVA =
    document.getElementById("aplicar_iva");

const precioMinimoHTML =
    document.getElementById("precio_minimo");

const formulario =
    document.getElementById("formVenta");


//=====================================
// COMPROBAR ELEMENTOS
//=====================================

console.log("Elementos ventas:", {
    formulario,
    subtotalHTML,
    descuentoHTML,
    ivaHTML,
    totalHTML,
    totalProductosHTML,
    descuentoInput,
    aplicarIVA
});


//=====================================
// FECHA DE HOY
//=====================================

function establecerFechaHoy() {

    const campoFecha =
        document.getElementById("fecha");

    if (!campoFecha) {
        return;
    }

    const hoy = new Date();

    const anio =
        hoy.getFullYear();

    const mes =
        String(
            hoy.getMonth() + 1
        ).padStart(2, "0");

    const dia =
        String(
            hoy.getDate()
        ).padStart(2, "0");

    campoFecha.value =
        `${anio}-${mes}-${dia}`;
}


//=====================================
// INICIO
//=====================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        establecerFechaHoy();

        actualizarResumen();

    }
);


//=====================================
// BUSCAR PRODUCTOS
//=====================================

inputBuscar.addEventListener(
    "input",
    async function () {

        const texto =
            inputBuscar.value.trim();


        if (texto.length < 2) {

            listaProductos.style.display =
                "none";

            listaProductos.innerHTML =
                "";

            return;
        }


        try {

            const respuesta =
                await fetch(
                    `/buscar_producto?q=${encodeURIComponent(texto)}`
                );


            if (!respuesta.ok) {

                throw new Error(
                    `HTTP ${respuesta.status}`
                );

            }


            const productos =
                await respuesta.json();


            listaProductos.innerHTML =
                "";


            if (
                productos.length === 0
            ) {

                listaProductos.innerHTML = `

                    <div class="item-producto-vacio">
                        No se encontraron productos
                    </div>

                `;

                listaProductos.style.display =
                    "block";

                return;
            }


            productos.forEach(
                producto => {

                    listaProductos.innerHTML += `

                        <div
                            class="item-producto"

                            data-id="${producto.id_producto}"

                            data-precio="${producto.precio_venta}"

                            data-costo="${producto.costo}"

                            data-stock="${producto.stock}"

                            data-codigo="${producto.codigo}"

                            data-nombre="${producto.nombre}"
                        >

                            <strong>
                                ${escapeHTML(producto.codigo)}
                            </strong>

                            <br>

                            ${escapeHTML(producto.nombre)}

                            <small>
                                Stock: ${producto.stock}
                            </small>

                        </div>

                    `;

                }
            );


            listaProductos.style.display =
                "block";


        }
        catch (error) {

            console.error(
                "Error buscando productos:",
                error
            );

        }

    }
);


//=====================================
// SELECCIONAR PRODUCTO
//=====================================

listaProductos.addEventListener(
    "click",
    function (e) {

        const item =
            e.target.closest(
                ".item-producto"
            );


        if (!item) {
            return;
        }


        productoSeleccionado = {

            id_producto:
                Number(
                    item.dataset.id
                ),

            codigo:
                item.dataset.codigo,

            nombre:
                item.dataset.nombre,

            precio:
                Number(
                    item.dataset.precio
                ),

            costo:
                Number(
                    item.dataset.costo
                ),

            stock:
                Number(
                    item.dataset.stock
                )

        };


        idProducto.value =
            productoSeleccionado.id_producto;


        precio.value =
            productoSeleccionado.precio;


        precio.min =
            productoSeleccionado.costo;


        precioMinimoHTML.textContent =
            `Precio mínimo: ${formatearMoneda(
                productoSeleccionado.costo
            )}`;


        inputBuscar.value =
            productoSeleccionado.nombre;


        listaProductos.innerHTML =
            "";

        listaProductos.style.display =
            "none";


        cantidad.focus();

    }
);


//=====================================
// CERRAR BUSCADOR
//=====================================

document.addEventListener(
    "click",
    function (e) {

        if (
            !e.target.closest(
                ".search-product"
            )
        ) {

            listaProductos.style.display =
                "none";

        }

    }
);


//=====================================
// VALIDAR PRECIO
//=====================================

function validarPrecio() {

    if (
        productoSeleccionado === null
    ) {

        return false;

    }


    const precioActual =
        Number(
            precio.value
        );


    const costo =
        Number(
            productoSeleccionado.costo
        );


    if (
        isNaN(precioActual) ||
        precioActual <= 0
    ) {

        alert(
            "Ingrese un precio válido."
        );

        precio.focus();

        return false;

    }


    if (
        precioActual < costo
    ) {

        alert(
            `El precio no puede ser inferior al costo de ${formatearMoneda(costo)}.`
        );

        precio.value =
            costo;

        precio.focus();

        return false;

    }


    return true;

}


//=====================================
// AGREGAR PRODUCTO
//=====================================

btnAgregar.addEventListener(
    "click",
    function () {

        if (
            productoSeleccionado === null
        ) {

            alert(
                "Seleccione un producto."
            );

            return;

        }


        if (
            !validarPrecio()
        ) {

            return;

        }


        const cant =
            parseInt(
                cantidad.value
            );


        if (
            isNaN(cant) ||
            cant <= 0
        ) {

            alert(
                "Cantidad inválida."
            );

            return;

        }


        if (
            cant >
            productoSeleccionado.stock
        ) {

            alert(
                "Stock insuficiente."
            );

            return;

        }


        const precioActual =
            Number(
                precio.value
            );


        // =================================
        // BUSCAR PRODUCTO EXISTENTE
        // =================================

        const existente =
            productosVenta.find(
                producto =>
                    producto.id_producto ===
                    productoSeleccionado.id_producto
            );


        if (existente) {

            const nuevaCantidad =
                existente.cantidad +
                cant;


            if (
                nuevaCantidad >
                productoSeleccionado.stock
            ) {

                alert(
                    "La cantidad total supera el stock disponible."
                );

                return;

            }


            existente.cantidad =
                nuevaCantidad;


            existente.precio =
                precioActual;


            existente.subtotal =
                existente.cantidad *
                existente.precio;

        }
        else {

            productosVenta.push({

                id_producto:
                    productoSeleccionado.id_producto,

                nombre:
                    productoSeleccionado.nombre,

                cantidad:
                    cant,

                precio:
                    precioActual,

                costo:
                    productoSeleccionado.costo,

                subtotal:
                    cant *
                    precioActual

            });

        }


        actualizarTabla();

        limpiarFormularioProducto();

    }
);


//=====================================
// ACTUALIZAR TABLA
//=====================================

function actualizarTabla() {

    detalleVenta.innerHTML =
        "";


    if (
        productosVenta.length === 0
    ) {

        detalleVenta.innerHTML = `

            <tr>

                <td
                    colspan="5"
                    class="empty"
                >
                    No hay productos agregados.
                </td>

            </tr>

        `;


        actualizarResumen();

        return;
    }


    productosVenta.forEach(
        function (producto, index) {

            detalleVenta.innerHTML += `

                <tr>

                    <td>
                        ${escapeHTML(
                            producto.nombre
                        )}
                    </td>

                    <td>
                        ${producto.cantidad}
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

                    <td>

                        <button
                            type="button"
                            onclick="eliminarProducto(${index})"
                            title="Eliminar"
                        >

                            <i
                                class="fa-solid fa-trash"
                            ></i>

                        </button>

                    </td>

                </tr>

            `;

        }
    );


    actualizarResumen();

}


//=====================================
// ELIMINAR PRODUCTO
//=====================================

function eliminarProducto(indice) {

    productosVenta.splice(
        indice,
        1
    );

    actualizarTabla();

}

window.eliminarProducto =
    eliminarProducto;


//=====================================
// SUBTOTAL
//=====================================

function calcularSubtotal() {

    let subtotal = 0;


    productosVenta.forEach(
        function (producto) {

            subtotal +=
                Number(
                    producto.subtotal
                );

        }
    );


    return subtotal;

}


//=====================================
// PORCENTAJE DE DESCUENTO
//=====================================

function obtenerPorcentajeDescuento() {

    let porcentaje =
        Number(
            descuentoInput.value
        );


    if (
        isNaN(porcentaje) ||
        porcentaje < 0
    ) {

        porcentaje = 0;

    }


    if (
        porcentaje > 100
    ) {

        porcentaje = 100;

        descuentoInput.value = 100;

    }


    return porcentaje;

}


//=====================================
// VALOR DEL DESCUENTO
//=====================================

function calcularDescuento() {

    const subtotal =
        calcularSubtotal();


    const porcentaje =
        obtenerPorcentajeDescuento();


    return (
        subtotal *
        (porcentaje / 100)
    );

}


//=====================================
// IVA
//=====================================

function calcularIVA() {

    if (
        !aplicarIVA.checked
    ) {

        return 0;

    }


    const subtotal =
        calcularSubtotal();


    const descuento =
        calcularDescuento();


    const baseIVA =
        Math.max(
            subtotal - descuento,
            0
        );


    return (
        baseIVA * 0.19
    );

}


//=====================================
// TOTAL
//=====================================

function calcularTotal() {

    const subtotal =
        calcularSubtotal();


    const descuento =
        calcularDescuento();


    const iva =
        calcularIVA();


    const total =
        subtotal -
        descuento +
        iva;


    console.log({
        subtotal,
        descuento,
        iva,
        total
    });


    return total;

}


//=====================================
// ACTUALIZAR RESUMEN
//=====================================

function actualizarResumen() {

    const subtotal =
        calcularSubtotal();


    const descuento =
        calcularDescuento();


    const iva =
        calcularIVA();


    const total =
        calcularTotal();


    // =================================
    // TOTAL DE UNIDADES
    // =================================

    const totalUnidades =
        productosVenta.reduce(
            function (total, producto) {

                return (
                    total +
                    Number(
                        producto.cantidad
                    )
                );

            },
            0
        );


    totalProductosHTML.textContent =
        totalUnidades;


    // =================================
    // MOSTRAR VALORES
    // =================================

    subtotalHTML.textContent =
        formatearMoneda(
            subtotal
        );


    descuentoHTML.textContent =
        formatearMoneda(
            descuento
        );


    ivaHTML.textContent =
        formatearMoneda(
            iva
        );


    totalHTML.textContent =
        formatearMoneda(
            total
        );


    console.log(
        "RESUMEN ACTUALIZADO:",
        {
            unidades: totalUnidades,
            subtotal: subtotal,
            descuento: descuento,
            iva: iva,
            total: total
        }
    );

}


//=====================================
// CAMBIO DE DESCUENTO
//=====================================

descuentoInput.addEventListener(
    "input",
    actualizarResumen
);


//=====================================
// CAMBIO DE IVA
//=====================================

aplicarIVA.addEventListener(
    "change",
    actualizarResumen
);


//=====================================
// CAMBIO DE PRECIO
//=====================================

precio.addEventListener(
    "input",
    function () {

        if (
            productoSeleccionado === null
        ) {

            return;

        }


        const costo =
            Number(
                productoSeleccionado.costo
            );


        const precioActual =
            Number(
                precio.value
            );


        if (
            precioActual < costo
        ) {

            precioMinimoHTML.textContent =
                `El precio mínimo es ${formatearMoneda(costo)}`;

            precioMinimoHTML.classList.add(
                "price-error"
            );

        }
        else {

            precioMinimoHTML.textContent =
                `Precio mínimo: ${formatearMoneda(costo)}`;

            precioMinimoHTML.classList.remove(
                "price-error"
            );

        }

    }
);


//=====================================
// LIMPIAR PRODUCTO
//=====================================

function limpiarFormularioProducto() {

    productoSeleccionado =
        null;


    idProducto.value =
        "";


    inputBuscar.value =
        "";


    precio.value =
        "";


    precio.removeAttribute(
        "min"
    );


    precioMinimoHTML.textContent =
        "Selecciona un producto.";


    precioMinimoHTML.classList.remove(
        "price-error"
    );


    cantidad.value =
        1;


    inputBuscar.focus();

}


//=====================================
// LIMPIAR VENTA
//=====================================

function limpiarVentaCompleta() {

    productosVenta = [];


    formulario.reset();


    establecerFechaHoy();


    cantidad.value =
        1;


    descuentoInput.value =
        0;


    aplicarIVA.checked =
        false;


    limpiarFormularioProducto();


    actualizarTabla();

}


//=====================================
// REGISTRAR VENTA
//=====================================

formulario.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();


        if (
            productosVenta.length === 0
        ) {

            alert(
                "Debe agregar al menos un producto."
            );

            return;

        }


        // =================================
        // VALIDAR PRECIOS
        // =================================

        const precioInvalido =
            productosVenta.some(
                function (producto) {

                    return (
                        Number(
                            producto.precio
                        ) <
                        Number(
                            producto.costo
                        )
                    );

                }
            );


        if (
            precioInvalido
        ) {

            alert(
                "Existe un producto con un precio inferior a su costo."
            );

            return;

        }


        const subtotal =
            calcularSubtotal();


        const porcentajeDescuento =
            obtenerPorcentajeDescuento();


        const descuento =
            calcularDescuento();


        const iva =
            calcularIVA();


        const total =
            calcularTotal();


        const datos = {

            cliente:
                document.getElementById(
                    "cliente"
                ).value,

            documento:
                document.getElementById(
                    "documento"
                ).value,

            fecha:
                document.getElementById(
                    "fecha"
                ).value,

            metodo_pago:
                document.getElementById(
                    "metodo_pago"
                ).value,

            subtotal:
                subtotal,

            // IMPORTANTE:
            // Se envía el valor monetario
            // del descuento, no el porcentaje.

            descuento:
                descuento,

            iva:
                iva,

            total:
                total,

            observaciones:
                document.getElementById(
                    "observaciones"
                ).value,

            productos:
                productosVenta

        };


        console.log(
            "DATOS ENVIADOS:",
            {
                porcentajeDescuento,
                ...datos
            }
        );


        try {

            const respuesta =
                await fetch(
                    "/registrar_venta",
                    {

                        method:
                            "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                datos
                            )

                    }
                );


            const resultado =
                await respuesta.json();


            console.log(
                "RESPUESTA FLASK:",
                resultado
            );


            if (
                resultado.ok
            ) {

                alert(
                    resultado.mensaje
                );


                if (
                    resultado.factura_url
                ) {

                    window.open(
                        resultado.factura_url,
                        "_blank"
                    );

                }


                limpiarVentaCompleta();

            }
            else {

                alert(
                    resultado.mensaje ||
                    "No fue posible registrar la venta."
                );

            }

        }
        catch (error) {

            console.error(
                "Error al registrar la venta:",
                error
            );


            alert(
                "Error al registrar la venta."
            );

        }

    }
);


//=====================================
// FORMATEAR MONEDA
//=====================================

function formatearMoneda(valor) {

    const numero =
        Number(
            valor
        ) || 0;


    return (
        "$" +
        numero.toLocaleString(
            "es-CO",
            {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }
        )
    );

}


//=====================================
// ESCAPAR HTML
//=====================================

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