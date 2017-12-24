from flask import Flask, render_template, request, session
import random
from sqlalchemy.engine import create_engine
from flask_session import Session



app = Flask(__name__)
sess = Session()
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'redsfsfsfsfis'
sess.init_app(app)


def dbconnect():
    engine = create_engine('postgres://balajidr:spiderman@localhost:5432/dalal')
    connection = engine.connect()
    return connection


def dbclose(connection):
    connection.close()
    return


@app.route('/')
def league():

    return render_template("index.html")


@app.route('/league', methods=['post'])
def leaguee():
    username = request.form['username']
    session['username'] = username
    connection = dbconnect()
    result = connection.execute("SELECT username from users")
    for row in result:
        if username in row['username']:
            session['loggedin'] = True
            return render_template("mainleague.html")




@app.route('/createleague')
def createleague():
    return render_template("createleague.html")


@app.route('/joinleague')
def joinleague():
    return render_template("joinleague.html")


@app.route('/createmyleagues', methods=['post', 'get'])
def myleagues():
    leagueName = request.form['name']
    print(leagueName )
    leagueid = ''.join(random.choice('0123456789ABCDEF') for i in range(5))
    print(leagueid)
    val = 0
    connection = dbconnect()
    query = "INSERT INTO members(leagueid,userid) VALUES(%s,%s)"
    args = (leagueid, session['username'])
    connection.execute(query, args)
    print("inserted into members")
    members = []
    query = "SELECT userid FROM members WHERE leagueid=%s"
    args = (leagueid)
    result = connection.execute(query, args)
    for row in result:
        temp = row['userid']
        members.append(temp)
    print("got all the users from the league")
    print(members)

    for user in members:
        args = (user)
        query = "SELECT val FROM users WHERE username=%s"
        result = connection.execute(query,args)
        for row in result:
            val = val + row['val']

    print(val)

    query = "INSERT INTO leagueinfo(leagueid,val) VALUES (%s,%s)"
    args = (leagueid,val)
    connection.execute(query,args)

    print("LEAGUE " + str(leagueid) + " VALUE " + str(val))
    message = "Id for the last created league was " + str(leagueid)

    return render_template("index.html",message=message)


@app.route('/joinleaguee',methods=['post','get'])
def joinleaguee():
    leagueid = request.form['leagueid']

    connection = dbconnect()
    query = "SELECT * FROM leagueinfo WHERE leagueid=%s"
    args = (leagueid)
    result = connection.execute(query,args)

    if result:
        query = "INSERT INTO members(leagueid,userid) VALUES(%s,%s) "
        args = (leagueid, session['username'])
        connection.execute(query, args)

        members = []
        query = "SELECT userid FROM members WHERE leagueid=%s"
        args = (leagueid)
        result = connection.execute(query, args)
        for row in result:
            temp = row['userid']
            members.append(temp)
        print("got all the users from the league")
        print(members)
        val = 0
        for user in members:
            args = (user)
            query = "SELECT val FROM users WHERE username=%s"
            result = connection.execute(query, args)
            for row in result:
                val = val + row['val']

        print(val)

        query = "UPDATE leagueinfo SET val=%s WHERE leagueid=%s"
        args = (val, leagueid)
        connection.execute(query, args)
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
