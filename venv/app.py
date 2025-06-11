from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from functions.clientes import register_client as cliente_logic
from functions.sedes import sede_logic
from functions.planes import plan_logic
from functions.pagos import pago_logic

app = Flask(__name__)

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'solimano123'
app.config['MYSQL_DB'] = 'BD_GYM'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'soliman0123'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Rutas para Clientes
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    result = cliente_logic(mysql, request)
    if result:
        return result
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

# Rutas para Pagos
@app.route('/pagos', methods=['GET', 'POST'])
def pagos():
    result = pago_logic(mysql, request)
    if result:
        return result
    return render_template('pagos.html')

if __name__ == '__main__':
    app.run(debug=True)