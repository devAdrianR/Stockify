const inputBuscar = document.getElementById("buscar_producto");
const listaProductos = document.getElementById("lista_productos");

const idProducto = document.getElementById("id_producto");
const precio = document.getElementById("precio");
const cantidad = document.getElementById("cantidad");

inputBuscar.addEventListener("input", async () => {

    const texto = inputBuscar.value.trim();

    if (texto.length < 2) {

        listaProductos.style.display = "none";
        listaProductos.innerHTML = "";

        return;
    }

    try {

        const respuesta = await fetch(`/buscar_producto?q=${encodeURIComponent(texto)}`);

        const productos = await respuesta.json();

        listaProductos.innerHTML = "";

        if (productos.length === 0) {

            listaProductos.innerHTML = `
                <div class="item-producto-vacio">
                    No se encontraron productos
                </div>
            `;

            listaProductos.style.display = "block";

            return;
        }

        productos.forEach(producto => {

            listaProductos.innerHTML += `
                <div class="item-producto"
                    data-id="${producto.id_producto}"
                    data-precio="${producto.precio_venta}"
                    data-stock="${producto.stock}">

                    <strong>${producto.codigo}</strong>

                    <br>

                    ${producto.nombre}

                    <small>
                        Stock: ${producto.stock}
                    </small>

                </div>
            `;

        });

        listaProductos.style.display = "block";

    }

    catch(error){

        console.log(error);

    }

});

listaProductos.addEventListener("click", (e)=>{

    const item = e.target.closest(".item-producto");

    if(!item) return;

    idProducto.value = item.dataset.id;

    precio.value = item.dataset.precio;

    inputBuscar.value = item.childNodes[4].textContent.trim();

    listaProductos.innerHTML = "";

    listaProductos.style.display = "none";

    cantidad.focus();

});

document.addEventListener("click",(e)=>{

    if(!e.target.closest(".search-product")){

        listaProductos.style.display="none";

    }

});