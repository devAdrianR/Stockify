/* =====================================================
   PRODUCTOS MÁS VENDIDOS - JAVASCRIPT
   Stockify
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    console.log("=================================");
    console.log("PRODUCTOS MÁS VENDIDOS");
    console.log("=================================");


    // =================================================
    // ELEMENTOS
    // =================================================

    const formulario = document.querySelector("form");

    const fechaInicio = document.getElementById("fecha_inicio");

    const fechaFin = document.getElementById("fecha_fin");


    // =================================================
    // VERIFICAR ELEMENTOS
    // =================================================

    if (!formulario) {

        console.error(
            "No se encontró el formulario del reporte."
        );

        return;
    }


    console.log(
        "Formulario encontrado correctamente."
    );


    // =================================================
    // VALIDAR FORMULARIO
    // =================================================

    formulario.addEventListener("submit", function (event) {

        const inicio = fechaInicio.value;

        const fin = fechaFin.value;


        // =============================================
        // SI SE INGRESA FECHA FINAL SIN INICIAL
        // =============================================

        if (!inicio && fin) {

            event.preventDefault();

            alert(
                "Debes seleccionar primero la fecha inicial."
            );

            fechaInicio.focus();

            return;
        }


        // =============================================
        // SI SE INGRESA FECHA INICIAL SIN FINAL
        // =============================================

        if (inicio && !fin) {

            event.preventDefault();

            alert(
                "Debes seleccionar la fecha final."
            );

            fechaFin.focus();

            return;
        }


        // =============================================
        // VALIDAR ORDEN DE FECHAS
        // =============================================

        if (inicio && fin) {

            if (inicio > fin) {

                event.preventDefault();

                alert(
                    "La fecha inicial no puede ser posterior a la fecha final."
                );

                fechaInicio.focus();

                return;
            }

        }


        console.log(
            "Consultando productos más vendidos..."
        );

        console.log(
            "Fecha inicial:",
            inicio || "Sin filtro"
        );

        console.log(
            "Fecha final:",
            fin || "Sin filtro"
        );

    });


    // =================================================
    // ANIMACIÓN DE TABLA
    // =================================================

    const filas = document.querySelectorAll(
        "tbody tr"
    );


    filas.forEach(function (fila, index) {

        fila.style.animationDelay =
            `${index * 0.04}s`;

    });


    // =================================================
    // MENSAJE DE CARGA AL BUSCAR
    // =================================================

    formulario.addEventListener("submit", function () {

        const boton = formulario.querySelector(
            ".btn-search"
        );


        if (boton) {

            boton.disabled = true;

            boton.innerHTML = `
                <i class="fa-solid fa-spinner fa-spin"></i>
                Buscando...
            `;

        }

    });


    console.log(
        "JavaScript de productos más vendidos cargado."
    );

});
