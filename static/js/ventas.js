console.log("JS cargado correctamente");

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

const formulario =
    document.getElementById("formVenta");


//=====================================
// BUSCAR PRODUCTOS
//=====================================

inputBuscar.addEventListener("input", async () => {

    const texto =
        inputBuscar.value.trim();


    if (texto.length < 2) {

        listaProductos.style.display = "none";

        listaProductos.innerHTML = "";

        return;
    }


    try {

        const respuesta = await fetch(
            `/buscar_producto?q=${encodeURIComponent(texto)}`
        );


        if (!respuesta.ok) {

            throw new Error(
                `HTTP ${respuesta.status}`
            );

        }


        const productos =
            await respuesta.json();


        listaProductos.innerHTML = "";


        if (productos.length === 0) {

            listaProductos.innerHTML = `

                <div class="item-producto-vacio">

                    No se encontraron productos

                </div>

            `;

            listaProductos.style.display =
                "block";

            return;
        }


        productos.forEach(producto => {

            listaProductos.innerHTML += `

                <div
                    class="item-producto"
                    data-id="${producto.id_producto}"
                    data-precio="${producto.precio_venta}"
                    data-stock="${producto.stock}"
                    data-codigo="${producto.codigo}"
                    data-nombre="${producto.nombre}"
                >

                    <strong>
                        ${producto.codigo}
                    </strong>

                    <br>

                    ${producto.nombre}

                    <small>

                        Stock: ${producto.stock}

                    </small>

                </div>

            `;

        });


        listaProductos.style.display =
            "block";

    }

    catch (error) {

        console.error(
            "Error buscando productos:",
            error
        );

    }

});


//=====================================
// SELECCIONAR PRODUCTO
//=====================================

listaProductos.addEventListener(
    "click",
    (e) => {

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

            stock:
                Number(
                    item.dataset.stock
                )

        };


        idProducto.value =
            productoSeleccionado.id_producto;


        precio.value =
            productoSeleccionado.precio;


        inputBuscar.value =
            productoSeleccionado.nombre;


        listaProductos.innerHTML = "";

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
    (e) => {

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
// AGREGAR PRODUCTO
//=====================================

btnAgregar.addEventListener(
    "click",
    () => {

        if (
            productoSeleccionado === null
        ) {

            alert(
                "Seleccione un producto."
            );

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


        // =================================
        // EVITAR PRODUCTOS REPETIDOS
        // =================================

        const existente =
            productosVenta.find(
                p =>
                    p.id_producto ===
                    productoSeleccionado.id_producto
            );


        if (existente) {

            const nuevaCantidad =
                existente.cantidad + cant;


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
                    productoSeleccionado.precio,

                subtotal:
                    cant *
                    productoSeleccionado.precio

            });

        }


        actualizarTabla();

        limpiarFormularioProducto();

    }
);


//=====================================
// TABLA
//=====================================

function actualizarTabla() {

    detalleVenta.innerHTML = "";


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
        (producto, index) => {

            detalleVenta.innerHTML += `

                <tr>

                    <td>
                        ${producto.nombre}
                    </td>

                    <td>
                        ${producto.cantidad}
                    </td>

                    <td>
                        $${producto.precio.toLocaleString(
                            "es-CO"
                        )}
                    </td>

                    <td>
                        $${producto.subtotal.toLocaleString(
                            "es-CO"
                        )}
                    </td>

                    <td>

                        <button
                            type="button"
                            onclick="eliminarProducto(${index})"
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
// CALCULAR SUBTOTAL
//=====================================

function calcularSubtotal() {

    let subtotal = 0;


    productosVenta.forEach(
        producto => {

            subtotal +=
                Number(
                    producto.subtotal
                );

        }
    );


    return subtotal;

}


//=====================================
// CALCULAR IVA
//=====================================

function calcularIVA() {

    return calcularSubtotal() * 0.19;

}


//=====================================
// CALCULAR TOTAL
//=====================================

function calcularTotal() {

    return (
        calcularSubtotal() +
        calcularIVA()
    );

}


//=====================================
// RESUMEN
//=====================================

function actualizarResumen() {

    const subtotal =
        calcularSubtotal();


    const descuento = 0;


    const iva =
        calcularIVA();


    const total =
        subtotal -
        descuento +
        iva;


    totalProductosHTML.textContent =
        productosVenta.length;


    subtotalHTML.textContent =
        "$" +
        subtotal.toLocaleString(
            "es-CO"
        );


    descuentoHTML.textContent =
        "$" +
        descuento.toLocaleString(
            "es-CO"
        );


    ivaHTML.textContent =
        "$" +
        iva.toLocaleString(
            "es-CO"
        );


    totalHTML.textContent =
        "$" +
        total.toLocaleString(
            "es-CO"
        );

}


//=====================================
// LIMPIAR CONTROLES
//=====================================

function limpiarFormularioProducto() {

    productoSeleccionado = null;


    idProducto.value = "";


    inputBuscar.value = "";


    precio.value = "";


    cantidad.value = 1;


    inputBuscar.focus();

}


//=====================================
// LIMPIAR VENTA COMPLETA
//=====================================

function limpiarVentaCompleta() {

    productosVenta = [];


    actualizarTabla();


    formulario.reset();


    cantidad.value = 1;


    limpiarFormularioProducto();

}


//=====================================
// REGISTRAR VENTA
//=====================================

formulario.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();


        // =================================
        // VALIDAR PRODUCTOS
        // =================================

        if (
            productosVenta.length === 0
        ) {

            alert(
                "Debe agregar al menos un producto."
            );

            return;
        }


        // =================================
        // PREPARAR DATOS
        // =================================

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
                calcularSubtotal(),

            descuento:
                0,

            iva:
                calcularIVA(),

            total:
                calcularTotal(),

            observaciones:
                document.getElementById(
                    "observaciones"
                ).value,

            productos:
                productosVenta

        };


        console.log(
            "Datos de la venta:",
            datos
        );


        // =================================
        // ENVIAR A FLASK
        // =================================

        try {

            const respuesta =
                await fetch(
                    "/registrar_venta",
                    {

                        method: "POST",

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
                "Respuesta de Flask:",
                resultado
            );


            // =================================
            // VENTA CORRECTA
            // =================================

            if (
                resultado.ok
            ) {

                alert(
                    resultado.mensaje
                );


                // =================================
                // ABRIR FACTURA PDF
                // =================================

                if (
                    resultado.factura_url
                ) {

                    window.open(
                        resultado.factura_url,
                        "_blank"
                    );

                }
                else {

                    console.warn(
                        "No se recibió factura_url."
                    );

                }


                // =================================
                // LIMPIAR FORMULARIO
                // =================================

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