
// Control del sidebar
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            mainContent.classList.toggle('shifted');
            
            // Guardar preferencia en localStorage
            if (sidebar.classList.contains('show')) {
                localStorage.setItem('sidebarState', 'open');
            } else {
                localStorage.setItem('sidebarState', 'closed');
            }
        });
        
        // Cargar estado del sidebar
        if (window.innerWidth >= 992) {
            const sidebarState = localStorage.getItem('sidebarState');
            if (sidebarState === 'open' || sidebarState === null) {
                sidebar.classList.add('show');
                mainContent.classList.add('shifted');
            }
        }
    }
    
    // Ajustar dinámicamente el alto de los cards
    const equalizeCards = () => {
        const cardGroups = document.querySelectorAll('.card-group-equal');
        cardGroups.forEach(group => {
            let maxHeight = 0;
            const cards = group.querySelectorAll('.card');
            cards.forEach(card => {
                card.style.height = 'auto';
                if (card.offsetHeight > maxHeight) {
                    maxHeight = card.offsetHeight;
                }
            });
            cards.forEach(card => {
                card.style.height = maxHeight + 'px';
            });
        });
    };
    
    window.addEventListener('load', equalizeCards);
    window.addEventListener('resize', equalizeCards);

    // Función para crear gráficas con manejo de errores
    function createCharts() {
        try {
            // Gráfico de distribución por categoría
            const categoryCanvas = document.getElementById('categoryDistributionChart');
            if (categoryCanvas) {
                const categoryCtx = categoryCanvas.getContext('2d');
                new Chart(categoryCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Varillas de acero', 'Perfiles metálicos', 'Herramientas manuales', 'Materiales eléctricos', 'Tuberías y conexiones', 'Otros'],
                        datasets: [{
                            data: [28, 22, 18, 15, 12, 5],
                            backgroundColor: [
                                'rgba(52, 152, 219, 0.7)',
                                'rgba(46, 204, 113, 0.7)',
                                'rgba(241, 196, 15, 0.7)',
                                'rgba(155, 89, 182, 0.7)',
                                'rgba(231, 76, 60, 0.7)',
                                'rgba(149, 165, 166, 0.7)'
                            ],
                            borderColor: [
                                'rgba(52, 152, 219, 1)',
                                'rgba(46, 204, 113, 1)',
                                'rgba(241, 196, 15, 1)',
                                'rgba(155, 89, 182, 1)',
                                'rgba(231, 76, 60, 1)',
                                'rgba(149, 165, 166, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                            }
                        }
                    }
                });
            }

            // Gráfico de movimiento de inventario
            const movementCanvas = document.getElementById('inventoryMovementChart');
            if (movementCanvas) {
                const movementCtx = movementCanvas.getContext('2d');
                new Chart(movementCtx, {
                    type: 'line',
                    data: {
                        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
                        datasets: [
                            {
                                label: 'Entradas',
                                data: [1200, 1450, 980, 1820, 1950, 2100],
                                borderColor: 'rgba(46, 204, 113, 1)',
                                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Salidas',
                                data: [980, 1200, 850, 1500, 1750, 1900],
                                borderColor: 'rgba(231, 76, 60, 1)',
                                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Error al crear gráficas:', error);
        }
    }

    // Llamar a la función para crear gráficas
    createCharts();
});
