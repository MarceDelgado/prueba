document.addEventListener("DOMContentLoaded", function() {
    const accordionButtons = document.querySelectorAll(".accordion-button");

    accordionButtons.forEach(button => {
        button.addEventListener("click", function() {
            // Toggle activo para el botón
            this.classList.toggle("active");

            // Obtén el contenido del acordeón correspondiente
            const content = this.nextElementSibling;

            // Alterna la clase "open" para el contenido
            content.classList.toggle("open");

            // Cierra todos los otros acordeones
            accordionButtons.forEach(otherButton => {
                if (otherButton !== this) {
                    otherButton.classList.remove("active");
                    otherButton.nextElementSibling.classList.remove("open");
                }
            });
        });
    });
});

