document.addEventListener('DOMContentLoaded', function() {
    const filters = document.querySelectorAll('#changelist-filter details');
    fillters.forEach(filter => {
        filter.open = false; // Collapse all filter sections by default
    });
});