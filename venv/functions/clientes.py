from flask import flash, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

def register_client(mysql, request):
    if request.method == 'POST':
        datos = request.form
        cod_cliente = datos['cod_cliente']
        dni = datos['dni']
        nombres = datos['nombres']
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO CLIENTE (COD_CLIENTE, DNI, NOMBRES, APELLIDOS, 
                EMAIL, TELEFONO, SEXO, FECHA_NACIMIENTO)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (cod_cliente, dni, nombres, 
                 datos.get('apellidos', ''), 
                 datos.get('email', ''), 
                 datos.get('telefono', ''), 
                 datos.get('sexo', 'OTRO'), 
                 datos.get('fecha_nacimiento')))
            
            mysql.connection.commit()
            flash('Cliente registrado con éxito!', 'success')
            return redirect(url_for('index'))
            
        except MySQLdb.Error as e:
            mysql.connection.rollback()
            flash(f'Error al registrar cliente: {str(e)}', 'error')
            return None
    