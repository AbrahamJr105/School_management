// School Management System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initFormValidation();
    initTooltips();
    initModals();
    initSearchFunctionality();
    initPrintFunctionality();
    initCharts();
});

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Veuillez remplir tous les champs obligatoires.', 'danger');
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    
    // Clear previous validation
    field.classList.remove('is-invalid', 'is-valid');
    
    if (isRequired && !value) {
        field.classList.add('is-invalid');
        return false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    // Postal code validation
    if (field.name === 'cod_post' && value) {
        const postalRegex = /^\d{5}$/;
        if (!postalRegex.test(value)) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    // Grade validation
    if (field.name === 'note' && value) {
        const grade = parseFloat(value);
        if (isNaN(grade) || grade < 0 || grade > 20) {
            field.classList.add('is-invalid');
            return false;
        }
    }
    
    if (value) {
        field.classList.add('is-valid');
    }
    
    return true;
}

// Alert system
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.main-content .container');
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type}`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    alertContainer.insertBefore(alertElement, alertContainer.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertElement.parentElement) {
            alertElement.remove();
        }
    }, 5000);
}

// Tooltips initialization
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this, this.dataset.tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.position = 'absolute';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    tooltip.style.background = '#333';
    tooltip.style.color = 'white';
    tooltip.style.padding = '5px 10px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '12px';
    tooltip.style.zIndex = '1000';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Modal functionality
function initModals() {
    // Add modal functionality if needed
    const modalTriggers = document.querySelectorAll('[data-modal]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const modalId = this.dataset.modal;
            openModal(modalId);
        });
    });
}

// Search functionality
function initSearchFunctionality() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const targetTable = document.querySelector(this.dataset.target);
            
            if (targetTable) {
                const rows = targetTable.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });
}

// Print functionality
function initPrintFunctionality() {
    const printButtons = document.querySelectorAll('.btn-print');
    
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });
}

// Chart initialization
function initCharts() {
    // Gender distribution chart
    const genderChart = document.getElementById('genderChart');
    if (genderChart) {
        createGenderChart(genderChart);
    }
    
    // Grade distribution chart
    const gradeChart = document.getElementById('gradeChart');
    if (gradeChart) {
        createGradeChart(gradeChart);
    }
}

function createGenderChart(canvas) {
    const male = parseInt(canvas.dataset.male) || 0;
    const female = parseInt(canvas.dataset.female) || 0;
    
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: ['Hommes', 'Femmes'],
            datasets: [{
                data: [male, female],
                backgroundColor: ['#3498db', '#e74c3c'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Répartition par Genre'
                }
            }
        }
    });
}

function createGradeChart(canvas) {
    const passing = parseInt(canvas.dataset.passing) || 0;
    const failing = parseInt(canvas.dataset.failing) || 0;
    
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Admis', 'Ajournés'],
            datasets: [{
                label: 'Nombre d\'étudiants',
                data: [passing, failing],
                backgroundColor: ['#2ecc71', '#e74c3c'],
                borderColor: ['#27ae60', '#c0392b'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Résultats des Étudiants'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Image preview functionality
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Form submission with loading state
function submitWithLoading(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    submitButton.disabled = true;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Traitement...';
    
    // Re-enable after 5 seconds as fallback
    setTimeout(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    }, 5000);
}

// Utility functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}

function formatGrade(grade) {
    const numGrade = parseFloat(grade);
    if (isNaN(numGrade)) return grade;
    
    return numGrade.toFixed(2) + '/20';
}

function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}

// Email functionality
function sendEmail(type, data) {
    const formData = new FormData();
    formData.append('type', type);
    formData.append('data', JSON.stringify(data));
    
    fetch('/send-email/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Email envoyé avec succès!', 'success');
        } else {
            showAlert('Erreur lors de l\'envoi de l\'email.', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Erreur lors de l\'envoi de l\'email.', 'danger');
    });
}

// Chart image saving
function saveChartImage(chartId) {
    const canvas = document.getElementById(chartId);
    if (canvas) {
        const imageData = canvas.toDataURL('image/png');
        
        fetch('/save-chart-image/', {
            method: 'POST',
            body: JSON.stringify({ chart_image: imageData }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Graphique sauvegardé avec succès!', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
