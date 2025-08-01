document.addEventListener('DOMContentLoaded', () => {
    const dropdownWrapper = document.querySelector('.filter-dropdown-wrapper');
    const toggleBtn = document.getElementById('filter-toggle-btn');

    //Toggles the 'active' class on the wrapper (menu, btn and icon).
    toggleBtn.addEventListener('click', (event) => {
        // Prevents the button click from propagating to the document and closing the menu immediately.
        event.stopPropagation();
        dropdownWrapper.classList.toggle('active');
    });

    // Close the menu when clicking outside
    document.addEventListener('click', (event) => {
        if (!event.target.closest('.filter-dropdown-wrapper')) {
            dropdownWrapper.classList.remove('active');
        }
    });
});