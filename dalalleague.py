from flask import Flask, render_template, request, session
import random
from sqlalchemy.engine import create_engine
from flask_session import Session



app = Flask(__name__)
sess = Session()
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'podadukukkumandaya'
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


@app.route('/league', methods=['POST'])
def leaguee():
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            username = request.form['username']
            session['username'] = username
            connection = dbconnect()
            result = connection.execute("SELECT username from users")
            for row in result:
                if username in row['username']:
                    session['loggedin'] = True
                    dbclose(connection)
                    return render_template("mainleague.html")




@app.route('/createleague')
def createleague():
    return render_template("createleague.html")


@app.route('/joinleague')
def joinleague():
    return render_template("joinleague.html")


@app.route('/createmyleagues', methods=['POST'])
def myleagues():
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            leagueName = request.form['name']
            print(leagueName)
            leagueid = ''.join(random.choice('0123456789ABCDEF') for i in range(5))
            print(leagueid)
            connection = dbconnect()
            query = "SELECT leagueid FROM members"
            result = connection.execute(query)
            for row in result:
                if leagueid in row['leagueid']:
                    leagueid = ''.join(random.choice('0123456789ABCDEF') for i in range(5))
            val = 0
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

            query = "INSERT INTO leagueinfo(leagueid,val,leaguename) VALUES (%s,%s,%s)"
            args = (leagueid,val,leagueName)
            connection.execute(query,args)

            print("LEAGUE " + str(leagueid) + " VALUE " + str(val))
            message = "Id for the last created league "+str(leagueName)+" is " + str(leagueid)
            dbclose(connection)
            return render_template("index.html",message=message)


@app.route('/joinleaguee',methods=['post'])
def joinleaguee():
    leagueid = request.form['leagueid']

    connection = dbconnect()
    query = "SELECT leaguename FROM leagueinfo WHERE leagueid=%s"
    args = (leagueid)
    result = connection.execute(query, args)

    if result:

        query = "SELECT userid FROM members WHERE leagueid=%s"
        result = connection.execute(query,args)
        for row in result:
            if session['username'] in row['userid']:
                dbclose(connection)
                return render_template("index.html",message="You are already a member of the league!")


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
        dbclose(connection)
        return render_template("index.html")


@app.route('/leaguetable')
def leaguetable():

    connection = dbconnect()
    query = "SELECT leaguename,val FROM leagueinfo ORDER BY val DESC "
    result = connection.execute(query)
    tabledict={}

    for row in result:
        print(row['val'])
        tabledict[row['leaguename']] = row['val']

    desc = sorted(tabledict, key=tabledict.get, reverse=True)
    print(desc)
    print( tabledict)
    return render_template("leaguetable.html", table=tabledict,order=desc)


@app.route('/myownleagues')
def myownleague():
    connection = dbconnect()
    query="SELECT leagueid from members WHERE userid=%s"
    args=(session['username'])

    result = connection.execute(query,args)
    leaguesiampartof = []
    if result:
        for row in result:
            leaguesiampartof.append(row['leagueid'])
    print(leaguesiampartof)

    myleaguesinfo = {}
    for ids in leaguesiampartof:
        query = "SELECT leagueid,leaguename,val FROM leagueinfo WHERE leagueid=%s"
        args = (ids)

        result = connection.execute(query,args)
        for row in result:
            myleaguesinfo[row['leagueid']] = [row['leaguename'], row['val']]
    print(myleaguesinfo)



    return render_template("mainleague.html", leaguesda=myleaguesinfo)


@app.route('/myownleagues/<leagueid>',methods=['POST'])
def myleagueinfo(leagueid):
    if request.method == 'POST':
        if request.form['submit'] == "submit":
            connection = dbconnect()
            query = "SELECT userid FROM members WHERE leagueid=%s"
            args = (leagueid)
            members=[]
            result = connection.execute(query, args)
            for row in result:
                temp = row['userid']
                members.append(temp)
            print("got all the users from the league")
            print(members)
            info = {}
            for user in members:
                query = "SELECT username,val FROM users WHERE username=%s ORDER BY val DESC "
                args = (user)
                result = connection.execute(query, args)
                for row in result:
                    info[row['username']] = row['val']
            print(info)

            desc = sorted(info, key=info.get, reverse=True)

            return render_template("myleagueinfo.html",info=info,order=desc)

if __name__ == '__main__':
    app.run(debug=True)
