from flask import render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, jsonify
from functions.clientes import register_client as cliente_logic
import logging 
from functions.sedes import sede_logic
from functions.planes import plan_logic
from functions.pagos import registrar_pago as pago_logic  # Importa la nueva función
import traceback  # Para obtener detalles del error

# Configuración básica del logging (DEBE ir al inicio del archivo)
logging.basicConfig(level=logging.DEBUG) 

def configure_all_routes(app, mysql):
    # Ruta principal
    @app.route('/')
    def index():
        return render_template('index.html')

    # Rutas para Clientes (VERSIÓN CORREGIDA)
    @app.route('/clientes', methods=['GET', 'POST'])
    def clientes():
        if request.method == 'POST':
            try:
                # Procesar formulario
                success, message = cliente_logic(mysql, request)
                
                if not success:  # Si hay error
                    flash(message, 'error')
                else:  # Si es exitoso
                    flash('¡Registro exitoso!', 'success')
                    return redirect(url_for('pagos'))  # Redirección confirmada
                    
            except Exception as e:
                flash(f'Error inesperado: {str(e)}', 'error')
            
            return redirect(url_for('clientes'))  # Recarga si hay error
        
        return render_template('clientes.html')

    # Rutas para Sedes
    @app.route('/sedes', methods=['GET', 'POST'])
    def sedes():
        sedes = sede_logic(mysql, request)
        if request.method == 'POST' and isinstance(sedes, redirect):
            return sedes
        return render_template('sedes.html', sedes=sedes)

    # Rutas para Planes
    @app.route('/planes', methods=['GET', 'POST'])
    def planes():
        result = plan_logic(mysql, request)
        if result:
            return result
        return render_template('planes.html')
    
     # Ruta para la página de pagos (GET)
    @app.route('/pagos')
    def pagos():
        return render_template('pagos.html')  # Renderiza el formulario de pagos
        precio = request.args.get('precio', '0.00')  # Precio del plan seleccionado
        return render_template('pagos.html', precio=precio)

    # Ruta para procesar pagos (POST) - Versión integrada con tu MySQL
    @app.route('/procesar_pago', methods=['POST'])
    def procesar_pago():
        try:
            data = request.get_json()
            app.logger.debug(f"Datos recibidos: {data}")  # Log para debug

            # Validación básica
            required_fields = ['codPago', 'metodoPago', 'monto', 'fechaPago', 'fechaVencimiento']
            if not all(field in data for field in required_fields):
                return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400

            # Usa tu conexión MySQL existente (mejor que crear una nueva)
            cursor = mysql.connection.cursor()

            # Insertar pago
            query = """
            INSERT INTO PAGO (
                COD_PAGO, 
                ID_METODO, 
                MONTO, 
                FECHA_PAGO, 
                FECHA_VENCIMIENTO, 
                ESTADO
            ) VALUES (%s, %s, %s, %s, %s, 'COMPLETADO')
            """
            cursor.execute(query, (
                data['codPago'],
                data['metodoPago'],
                data['monto'],
                data['fechaPago'],
                data['fechaVencimiento']
            ))
            mysql.connection.commit()

            return jsonify({
                'success': True,
                'message': '¡Pago registrado exitosamente! 🐉'
            })

        except mysql.connector.Error as err:
            mysql.connection.rollback()
            app.logger.error(f"Error en BD: {err}")
            return jsonify({
                'success': False,
                'message': f'Error en la base de datos: {err.msg}'
            }), 500

        except Exception as e:
            app.logger.error(f"Error inesperado: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Error inesperado: {str(e)}'
            }), 500

        finally:
            if 'cursor' in locals():
                cursor.close()
