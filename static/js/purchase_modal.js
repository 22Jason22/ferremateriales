document.addEventListener('DOMContentLoaded', function () {
    var purchaseModalEl = document.getElementById('purchaseModal');
    var purchaseModal = new bootstrap.Modal(purchaseModalEl);
    var purchaseModalBody = document.getElementById('purchaseModalBody');

    function loadForm(url) {
        purchaseModalBody.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Cargando...</span></div></div>';
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                purchaseModalBody.innerHTML = html;
                var form = purchaseModalBody.querySelector('form');
                if (form) {
                    form.addEventListener('submit', function (e) {
                        e.preventDefault();
                        var formData = new FormData(form);
                        fetch(form.action || url, {
                            method: form.method,
                            body: formData,
                            headers: {
                                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                            }
                        })
                        .then(response => {
                            if (response.redirected) {
                                purchaseModal.hide();
                                window.location.reload();
                            } else {
                                return response.text();
                            }
                        })
                        .then(html => {
                            if (html) {
                                purchaseModalBody.innerHTML = html;
                            }
                        })
                        .catch(error => {
                            console.error('Error submitting form:', error);
                        });
                    });
                }
            })
            .catch(error => {
                purchaseModalBody.innerHTML = '<p class="text-danger">Error loading form.</p>';
                console.error('Error loading form:', error);
            });
    }

    // Load form when modal is shown
    purchaseModalEl.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var url = button.getAttribute('data-url');
        if (url) {
            var title;
            if (url.includes('edit')) {
                title = 'Editar Orden de Compra';
            } else if (url.includes('detail')) {
                title = 'Detalle de Orden de Compra';
            } else {
                title = 'Nueva Orden de Compra';
            }
            document.getElementById('purchaseModalLabel').textContent = title;
            loadForm(url);
        }
    });

    // Clear modal content when hidden
    purchaseModalEl.addEventListener('hidden.bs.modal', function () {
        purchaseModalBody.innerHTML = '';
    });
});
