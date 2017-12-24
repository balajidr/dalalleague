from flask import Flask,render_template,request
import requests
app = Flask(__name__)





@app.route('/')
def league():
    return render_template("index.html")

@app.route('/myleagues',methods=['post','get'])
def myleagues():
    leaguetype = request.form['type']
    leagueName = request.form['name']




if __name__ == '__main__':
    app.run()
