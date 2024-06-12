document.addEventListener('DOMContentLoaded', (event) => {
    const dropdownButton = document.getElementById('dropdownMenuButton');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    dropdownButton.addEventListener('click', () => {
        dropdownMenu.classList.toggle('show');
    });

    document.addEventListener('click', (event) => {
        if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });

    const checkboxes = dropdownMenu.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateButtonLabel);
    });

    function updateButtonLabel() {
        const selectedOptions = Array.from(checkboxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);
        if (selectedOptions.length > 0) {
            dropdownButton.textContent = selectedOptions.join(', ');
        } else {
            dropdownButton.textContent = 'TYPE FICHIER';
        }
    }
});