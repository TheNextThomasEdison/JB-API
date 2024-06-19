import os

from app import app
from flask_mysqldb import MySQL
# from dotenv import load_dotenv, dotenv_values
#
# load_dotenv()

# MySQL database connection credentials
db_user = os.environ["DB_PASSWORD"]
db_password = os.environ["DB_USERNAME"]
db_name = os.environ["DB_NAME"]
db_host = os.environ['DB_HOST']

# Create a MySQL connection
_mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = db_user
app.config['MYSQL_DATABASE_PASSWORD'] = db_password
app.config['MYSQL_DATABASE_DB'] = db_name
app.config['MYSQL_DATABASE_HOST'] = db_host
app.config['MYSQL_PORT'] = 3306
# _mysql.init_app(app)

# Create REST API CRUD operation

