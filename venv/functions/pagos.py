from flask import flash, redirect, url_for
import MySQLdb
from datetime import datetime
import logging

def registrar_pago(mysql, request_data):
    """
    Registra un pago en la base de datos.
    """
    try:
        cursor = mysql.connection.cursor()
        
        query = """
        INSERT INTO PAGO (
            COD_PAGO, ID_METODO, MONTO, 
            FECHA_PAGO, FECHA_VENCIMIENTO, ESTADO
        ) VALUES (%s, %s, %s, %s, %s, 'COMPLETADO')
        """
        cursor.execute(query, (
            request_data['codPago'],
            request_data['metodoPago'],
            request_data['monto'],
            request_data['fechaPago'],
            request_data['fechaVencimiento']
        ))
        mysql.connection.commit()
        
        return True, "Pago registrado exitosamente"
        
    except mysql.connector.Error as err:
        mysql.connection.rollback()
        logging.error(f"Error MySQL: {err}")
        return False, f"Error en la base de datos: {err.msg}"
        
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return False, f"Error inesperado: {str(e)}"
        
    finally:
        cursor.close()