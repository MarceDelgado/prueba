document.addEventListener('DOMContentLoaded', function() {
    const accordionButtons = document.querySelectorAll('.accordion-button');

    accordionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const icon = button.querySelector('.toggle-icon');
            icon.classList.toggle('rotate');
        });
    });
});