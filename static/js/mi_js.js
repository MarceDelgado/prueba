document.addEventListener('DOMContentLoaded', function () {
    const accordionButtons = document.querySelectorAll('.accordion-button');

    accordionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const icon = button.querySelector('.toggle-icon');
            icon.classList.toggle('rotate');
        });
    });
});

/*MENU USUARIO */
document.getElementById('scrollBtn').addEventListener('click', function () {
    document.getElementById('contenido').scrollIntoView();
});

// CARRUSEL AUTOMÁTICO
document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll(".accordion-item");
    let index = 0;
    const total = items.length;

    setInterval(() => {
        items.forEach((item) => item.style.flex = "1");
        items[index].style.flex = "3";
        items[index].querySelector("img").style.transform = "scale(1.1)";
        index = (index + 1) % total;
    }, 3000);
});

const backToTopBtn = document.getElementById("backToTopBtn");

window.addEventListener("scroll", function () {
    if (window.scrollY > 200) {
        backToTopBtn.style.display = "flex";
    } else {
        backToTopBtn.style.display = "none";
    }
});

backToTopBtn.addEventListener("click", function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});