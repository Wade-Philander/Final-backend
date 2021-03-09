from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# def drop():
#      app = Flask(__name__)
#      connection = sqlite3.connect('Users.db')
#      connection.execute("DROP TABLE users;")
#      print("DROPPED")
#      connection.close()
    
# drop()
    
                
def create_database_tables():
    connection = sqlite3.connect('Users.db')
    print("Databases has opened")
    c = connection.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, password TEXT, city TEXT)")
    print("Created user table successfully")
    c.execute("SELECT * FROM users")
    print(c.fetchall())
    connection.close()
create_database_tables()

#*******************************************  ADD NEW USER  ******************************************************************
@app.route('/')
@app.route('/add-new-user/', methods=['POST'])
def new_user():
    try:
        post_data = request.get_json()
        name = post_data['name']
        username = post_data['username']
        password = post_data['password']
        city = post_data['city']

        with sqlite3.connect('Users.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(name, username, password, city) VALUES (?, ?, ?, ?)", (name, username, password, city))
            con.commit()
            msg = username + " was successfully added to the database."
            print("New user has been added")
    except Exception as e:
        con.rollback()
        msg = "Error occurred: " +str(e)
    finally:
        con.close()
    return jsonify (msg = msg)

#**************************************************  SHOW USERS DATABASE  **************************************************************
@app.route('/')
@app.route('/show-users/', methods=["GET"])

def show_users():
    try:
        with sqlite3.connect('Users.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * From users")
            records = cur.fetchall()
            for i in records:
                print(i)
            print("Here are the users")

    except Exception as e:
        con.rollback()
        print("There was an error fetching users: " +str(e))

    finally:
        con.close()
    return jsonify (records)

#************************************* SHOW PROFILE*********************************************************
@app.route('/show_profile/', methods=['GET'])
def show_profile():
    try:
        post_data = request.get_json()
        name = post_data['name']
        username = post_data['username']

        with sqlite3.connect('Users.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM users where name = ? and username = ?" (name, username) ) 
            records = cur.fetchone()
            print("profile shown")

    except Exception as e:
        con.rollback()
        print("Can't view profile: " +str(e))

    finally:
        con.close()
    return jsonify (records)

#*************************************LOGIN PAGE*********************************************************

@app.route('/login-user/', methods=['GET'])

def login():
    try:
        with sqlite3.connect('Users.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * From users")
            row = cur.fetchall()
    except Exception as e:
        print("Error: " + str(e))
    return jsonify (row)


# *****************************************************DELETE PROFILE**********************************************

 @app.route('/delete-user/<int:id>/', methods=["DELETE"])
 def delete_user(id):

     msg = None
     try:
         with sqlite3.connect('Users.db') as con:
             cur = con.cursor()
             cur.execute("DELETE FROM student WHERE id=" + str(id))
             con.commit()
             msg = "Your Profile was deleted successfully from the database."
     except Exception as e:
         con.rollback()
         msg = "Error occurred when deleting a student in the database: " + str(e)
     finally:
         con.close()
         return jsonify(msg=msg)