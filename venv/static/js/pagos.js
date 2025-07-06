document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-generar código de pago (ej: "PAGO042")
    const generarCodigo = () => {
        const randomNum = Math.floor(Math.random() * 90) + 10;
        return `PAGO${randomNum}`;
    };

    // 2. Mostrar/ocultar campos de tarjeta
    const metodoPago = document.getElementById('metodoPago');
    const tarjetaFields = document.getElementById('tarjetaFields');

    metodoPago.addEventListener('change', () => {
        tarjetaFields.style.display = metodoPago.value === "1" ? "block" : "none";
    });

    // 3. Manejar envío del formulario
    document.getElementById('pagoForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Datos REALES que se enviarán a la BD
        const datosReales = {
            codPago: generarCodigo(),
            metodoPago: metodoPago.value,
            monto: document.getElementById('monto').value,
            fechaPago: new Date().toISOString().split('T')[0], // Fecha actual
            fechaVencimiento: new Date(new Date().setMonth(new Date().getMonth() + 1))
                             .toISOString().split('T')[0]      // Fecha +1 mes
        };

        try {
            const response = await fetch('/procesar_pago', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosReales)
            });

            const resultado = await response.json();
            const mensaje = document.getElementById('mensaje');
            
            if (resultado.success) {
                mensaje.innerHTML = `
                    <div class="success">
                        <i class="fas fa-check-circle"></i> ${resultado.message}
                    </div>
                `;
                document.getElementById('pagoForm').reset();
            } else {
                mensaje.innerHTML = `
                    <div class="error">
                        <i class="fas fa-times-circle"></i> ${resultado.message}
                    </div>
                `;
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById('mensaje').innerHTML = `
                <div class="error">
                    <i class="fas fa-times-circle"></i> Error al conectar con el servidor
                </div>
            `;
        }
    });

    // Inicializar campos
    tarjetaFields.style.display = "none"; // Ocultar tarjeta inicialmente
});