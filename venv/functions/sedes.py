from flask import flash, redirect, url_for, render_template_string
import MySQLdb

def sede_logic(mysql, request):
    # Obtener todas las sedes para mostrar
    cursor = mysql.connection.cursor()
    
    # Consulta mejorada para obtener información completa
    cursor.execute('''
        SELECT s.*, u.DIRECCION, d.NOMBRE_DISTRITO, p.NOMBRE_PROVINCIA
        FROM SEDE s
        JOIN UBICACION u ON s.ID_UBICACION = u.ID_UBICACION
        JOIN DISTRITO d ON u.ID_DISTRITO = d.ID_DISTRITO
        JOIN PROVINCIA p ON u.ID_PROVINCIA = p.ID_PROVINCIA
    ''')
    sedes = cursor.fetchall()
    
    if request.method == 'POST':
        try:
            # Lógica para registrar nueva sede (si es necesario)
            pass
        except MySQLdb.Error as e:
            mysql.connection.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return sedes  # Retornamos las sedes para mostrar