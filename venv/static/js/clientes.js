// Validación del formulario
document.getElementById('registroForm').addEventListener('submit', function(e) {
    const requiredFields = ['cod_cliente', 'dni', 'nombres'];
    let isValid = true;

    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = 'red';
        } else {
            field.style.borderColor = '#ddd';
        }
    });

    if (!isValid) {
        e.preventDefault();
        alert('Por favor complete los campos requeridos marcados en rojo');
        return false;
    }

    // Deshabilitar el botón para evitar múltiples envíos
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registrando...';
});

// Validación en tiempo real para DNI
document.getElementById('dni').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '');
    if (this.value.length > 8) {
        this.value = this.value.slice(0, 8);
    }
});

// Validación en tiempo real para teléfono
document.getElementById('telefono').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '');
    if (this.value.length > 9) {
        this.value = this.value.slice(0, 9);
    }
});