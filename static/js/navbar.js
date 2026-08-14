document.addEventListener("DOMContentLoaded", function () {

    const userMenuButton =
        document.getElementById("userMenuButton");

    const userDropdown =
        document.getElementById("userDropdown");


    // ==========================================
    // VERIFICAR ELEMENTOS
    // ==========================================

    if (!userMenuButton || !userDropdown) {

        console.error(
            "No se encontraron los elementos del menú de usuario."
        );

        return;
    }


    console.log(
        "Dashboard JS cargado correctamente."
    );


    // ==========================================
    // ABRIR / CERRAR MENÚ
    // ==========================================

    userMenuButton.addEventListener(
        "click",
        function (event) {

            event.stopPropagation();

            userDropdown.classList.toggle("show");

        }
    );


    // ==========================================
    // CERRAR AL HACER CLICK FUERA
    // ==========================================

    document.addEventListener(
        "click",
        function (event) {

            if (
                !event.target.closest(".user-menu")
            ) {

                userDropdown.classList.remove("show");

            }

        }
    );


    // ==========================================
    // CERRAR CON ESC
    // ==========================================

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                userDropdown.classList.remove(
                    "show"
                );

            }

        }
    );

});