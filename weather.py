from flask import Flask, render_template, request, jsonify
import sqlite3


weather = Flask(__name__)


def create_database_tables():
    with sqlite3.connect('users.db') as connection:
        print("Databases has opened")

        connection.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER, username TEXT)")
        print("Created user table successfully")
        # cursor = connection.cursor()
        # cursor.execute('')
        # cursor.execute()
        #cursor = sql.commit()


#*******************************************  ADD NEW USER  ******************************************************************


@weather.route('/add-new-user/', methods=['POST'])
def new_user():
    if request.method =="POST":
        
        msg = None

        try:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            city = request.form['city']

            with sqlite3.connect('users.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users(name, username, password, city) VALUES (?, ?, ?, ?)", (name, username, password, city))
                con.commit()
                msg = name = "was successfully added to the database."
                print("New user has been added")

        except Exception as e:
            con.rollback()
            msg = "Error occurred: " +str(e)

        finally:
            con.close()
            return jsonify (msg = msg)


#**************************************************  SHOW USERS DATABASE  **************************************************************

@weather.route('/show-users/', methods=["GET"])

def show_users():
    records = []
    try:
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * From student")
            record = cur.fetchall()
            print("Here are the users")

    except Exception as e:
        con.rollback()
        print("There was an error fetching users: " +str(e))

    finally:
        con.close()
        return jsonify (records)



@weather.route('/login-user/', methods=['POST'])
def login_user():
    # get form data
    # check db 
    pass


#*******************************************************************************************************************************************************
#*******************************************************************************************************************************************************


@weather.route('/',methods=['GET'])
def get_weather_today():

    api_url ="http://api.openweathermap.org/data/2.5/forecast?q=London&appid=e30a3785da67bd9d83b65bf8933359b5"

    response= request.get(api_url)
    json_data=response.json()

    
    main_weather = json_data ['list'][2]['weather'][0]['main']
    describe_weather = json_data ['list'][2]['weather'][0]['description']
    min_weather = json_data ['list'][0]['main']['temp_min']
    max_weather = json_data ['list'][0]['main']['temp_max']

    weather_data = str(main_weather)+" "+str(describe_weather) +" "+ str(min_weather) +" "+ str(max_weather)
    
    print(weather_data)

    return weather_data

if __name__ =="__main__":
    weather.run()
