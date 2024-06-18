import os

from app import app
from flask_mysqldb import MySQL

# Create a MySQL connection
_mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = 'rest-api'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# _mysql.init_app(app)

# Create REST API CRUD operation

