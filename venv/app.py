from flask import Flask
from flask_mysqldb import MySQL
from routes.routes import configure_all_routes
from dotenv import load_dotenv
import os

# Cargamos variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración MySQL desde variables de entorno
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = os.getenv('SECRET_KEY')

mysql = MySQL(app)
configure_all_routes(app, mysql)

if __name__ == '__main__':
    app.run(debug=True)