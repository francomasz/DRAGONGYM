from flask import flash, redirect, url_for
import MySQLdb
from datetime import datetime

def pago_logic(mysql, request):
    if request.method == 'POST':
        try:
            cursor = mysql.connection.cursor()
            
            cod_pago = request.form['cod_pago']
            id_metodo = request.form['id_metodo']
            monto = request.form['monto']
            fecha_pago = request.form.get('fecha_pago', datetime.now().date())
            fecha_vencimiento = request.form['fecha_vencimiento']
            
            cursor.execute('''
                INSERT INTO PAGO (COD_PAGO, ID_METODO, MONTO, FECHA_PAGO, FECHA_VENCIMIENTO)
                VALUES (%s, %s, %s, %s, %s)
            ''', (cod_pago, id_metodo, monto, fecha_pago, fecha_vencimiento))
            
            mysql.connection.commit()
            flash('Pago registrado con éxito!', 'success')
            return redirect(url_for('pagos'))
            
        except MySQLdb.Error as e:
            mysql.connection.rollback()
            flash(f'Error al registrar pago: {str(e)}', 'error')
    
    return None