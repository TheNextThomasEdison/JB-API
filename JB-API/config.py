import os
import socket

from app import app
from flask_mysqldb import MySQL
from dotenv import load_dotenv, dotenv_values

load_dotenv('sens_info.env')

host_name = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(host_name)

# MySQL database connection credentials
db_user = os.environ["DB_PASSWORD"]
db_password = os.environ["DB_USERNAME"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]

# Create a MySQL connection
app.config['MYSQL_USER'] = db_user
app.config['MYSQL_PASSWORD'] = db_password
app.config['MYSQL_HOST'] = IP_ADDRESS
app.config['MYSQL_DB'] = db_name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
_mysql = MySQL(app)

# _mysql.init_app(app)

# Create REST API CRUD operation

