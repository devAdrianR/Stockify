document.addEventListener("DOMContentLoaded", function () {

    const fecha = document.getElementById("fecha");

    // Colocar automáticamente la fecha actual
    if (fecha && !fecha.value) {

        const hoy = new Date();

        const year = hoy.getFullYear();
        const month = String(hoy.getMonth() + 1).padStart(2, "0");
        const day = String(hoy.getDate()).padStart(2, "0");

        fecha.value = `${year}-${month}-${day}`;
    }


    const formulario = document.getElementById("ingresoForm");

    if (formulario) {

        formulario.addEventListener("submit", function (event) {

            const monto = document.getElementById("monto").value;

            if (parseFloat(monto) <= 0) {

                event.preventDefault();

                alert("El monto debe ser mayor que 0.");

            }

        });

    }

});