const buscador = document.getElementById("buscarProducto");
const filtro = document.getElementById("filtroBusqueda");
const tabla = document.getElementById("tablaProductos");

async function buscarProductos() {

    const texto = buscador.value.trim();
    const tipo = filtro.value;

    const respuesta = await fetch(
        `/buscar_productos?texto=${encodeURIComponent(texto)}&filtro=${tipo}`
    );

    const datos = await respuesta.json();

    tabla.innerHTML = "";

    if (!datos.ok || datos.productos.length === 0) {

        tabla.innerHTML = `
            <tr>
                <td colspan="8" class="empty">
                    No se encontraron productos.
                </td>
            </tr>
        `;

        return;
    }

    datos.productos.forEach(producto => {

        tabla.innerHTML += `

        <tr>

            <td>${producto.codigo}</td>

            <td>${producto.nombre}</td>

            <td>${producto.categoria}</td>

            <td>$${producto.costo}</td>

            <td>$${producto.precio_venta}</td>

            <td>${producto.stock}</td>

            <td>

                ${
                    producto.estado == 1

                    ?

                    `<span class="status active">
                        Activo
                    </span>`

                    :

                    `<span class="status inactive">
                        Inactivo
                    </span>`
                }

            </td>

            <td class="actions">

                <a href="/editar_producto/${producto.id_producto}" class="edit">
                    <i class="fa-solid fa-pen"></i>
                </a>

                <a href="#" class="view">
                    <i class="fa-solid fa-eye"></i>
                </a>

                ${
                    producto.estado == 1

                    ?

                    `<a href="/desactivar_producto/${producto.id_producto}" class="delete">
                        <i class="fa-solid fa-box-archive"></i>
                    </a>`

                    :

                    `<a href="/activar_producto/${producto.id_producto}" class="activate">
                        <i class="fa-solid fa-box-open"></i>
                    </a>`
                }

            </td>

        </tr>

        `;
    });

}

let temporizador;

buscador.addEventListener("input", () => {

    clearTimeout(temporizador);

    temporizador = setTimeout(() => {

        buscarProductos();

    }, 300);

});

filtro.addEventListener("change", buscarProductos);