
from flask import render_template, redirect, url_for, flash
import MySQLdb

def plan_logic(mysql, request):
    # Lógica para registrar un plan nuevo (cuando el método es POST)
    if request.method == 'POST':
        try:
            cod_plan = request.form['cod_plan']
            nombre_plan = request.form['nombre_plan']
            descripcion = request.form['descripcion']
            duracion_semanas = request.form['duracion_semanas']

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO PLAN (COD_PLAN, NOMBRE_PLAN, DESCRIPCION, DURACION_SEMANAS)
                VALUES (%s, %s, %s, %s)
            """, (cod_plan, nombre_plan, descripcion, duracion_semanas))
            mysql.connection.commit()
            cur.close()
            flash('Plan registrado exitosamente', 'success')
            return redirect(url_for('planes'))
        except MySQLdb.IntegrityError:
            flash('Error: El código de plan ya existe', 'danger')
        except Exception as e:
            flash(f'Error al registrar el plan: {str(e)}', 'danger')
    
    # Lógica para mostrar los planes (cuando el método es GET)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Obtenemos TODOS los planes, ordenados por su ID
    cur.execute("SELECT * FROM PLAN ORDER BY ID_PLAN")
    planes_data = cur.fetchall()
    cur.close()
    
    # Enviamos la lista completa de planes al template bajo el nombre 'planes'
    return render_template('planes.html', planes=planes_data)