import os

import flask
import mysql.connector
import pymysql.cursors
from app import app
from config import _mysql
from flask import jsonify, flash, request


@app.route('/', methods=['GET', 'POST'])
def chat():
    """Retrieves user request"""
    _msg_received = request.get_json()  # or requests.json
    msg_subject = _msg_received["subject"]

    if msg_subject == 'register':
        return register(_msg_received)
    elif msg_subject == "login":
        return login(_msg_received)
    else:
        return jsonify('Invalid request')


def register(msg_received):
    try:
        _fullname = msg_received['fullname']
        _username = msg_received['username']
        _email = msg_received['email']
        _password = msg_received['password']
        _confirmed_password = msg_received['confirmed_password']
        _registration_date = msg_received['registration_date']

        if _fullname and _username and _email and _password and _confirmed_password and _registration_date:
            # conn = mysql.connector.connect(password=db_password, database=db_name,
            #                                user=db_user, host='localhost')
            # cursor = conn.cursor(dictionary=True)
            cursor = _mysql.connection.cursor()

            # Checking to see if the chosen username doesn't already exist
            select_query = "SELECT * FROM users where username = " + "'" + _username + "'"
            cursor.execute(select_query)
            records = cursor.fetchall()
            if len(records) != 0:
                return jsonify("Another user used the username. Please chose another username.")

            # Inserting user details into user table
            insert_query = ("INSERT INTO users(full_name, username, email, password, confirmed_password, "
                            "registration_date) VALUES(%s, %s, %s, MD5(%s), MD5(%s), %s)")
            insert_data = (_fullname, _username, _email, _password, _confirmed_password, _registration_date)
            try:
                cursor.execute(insert_query, insert_data)
                # conn.commit()
                _mysql.connection.commit()
                response = jsonify("User added successfully to J.B's community")
                response.status_code = 200
                # conn.commit()
                _mysql.connection.commit()
                cursor.close()
                return response
            except Exception as e:
                response = jsonify(f"Registration failed because: {str(e)}")
                return response
        else:
            return show_message()
    except Exception as e:
        return jsonify(f"The process wasn't able to complete because of {str(e)}")


def login(msg_received):
    username = msg_received["username"]
    if username:
        # conn = mysql.connector.connect(password=os.getenv('MYSQL_PASSWORD'), database='chat_db',
        #                                user=os.getenv('MYSQL_USERNAME'), host='localhost')
        # cursor = conn.cursor(dictionary=True)
        cursor = _mysql.connection.cursor()

        select_query = "SELECT full_name FROM users where username = " + "'" + username + "'"
        cursor.execute(select_query)
        records = cursor.fetchall()

        if len(records) == 0:
            return jsonify("Login failed")
        else:
            return jsonify(f"Login was a success {username}")
    else:
        return jsonify("No valid username was recognized")


@app.route('/users')
def users():
    """Gets the details of all users in the database"""
    try:
        conn = mysql.connector.connect(password=os.environ.get('MYSQL_PASSWORD'), database='chat_db',
                                       user=os.environ.get('MYSQL_USERNAME'), host='localhost')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, first_name, username, email, password, confirmed_password, "
                       "registration_date FROM users")
        user_rows = cursor.fetchall()
        response = jsonify(user_rows)
        response.status_code = 200
        conn.commit()
        cursor.close()
        return response
    except Exception as e:
        return jsonify(str(e))


@app.route('/users/<int:user_id>')
def user_details(user_id):
    try:
        conn = mysql.connector.connect(password=os.environ.get('MYSQL_PASSWORD'), database='chat_db', user='root',
                                       host='localhost')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, full_name, username, email, password, confirmed_password, registration_date FROM users WHERE username=%s", user_id)
        user_row = cursor.fetchone()
        response = jsonify(user_row)
        response.status_code = 200
        cursor.close()
        conn.commit()
        return response
    except Exception as e:
        return jsonify(str(e))


@app.route('/delete/', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = mysql.connector.connect(password=os.environ.get('MYSQL_PASSWORD'), database='chat_db', user='root',
                                       host='localhost')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        response = jsonify("User deleted successfully")
        response.status_code = 200
        cursor.close()
        conn.close()
        return response
    except Exception as e:
        return jsonify(str(e))


@app.errorhandler(404)
def show_message(error=None):
    message = {
        'status': 404,
        'message': 'Record not found' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080, debug=True)
