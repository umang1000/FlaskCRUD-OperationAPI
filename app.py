import flask
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask("myapp")
app.config["MONGO_URI"] = "mongodb://localhost:27017/task-manager"
app.config['MONGO_DBNAME'] = "task-manager"
mongo = PyMongo(app)
db = mongo.db

@app.route("/insert_one/<name>/<age>")
def insert_one(name, age):
    db.users.insert_one({'Name': name, 'Age':age})
    filt={'Name': 'utt'}
    users=db.users.find()
    output=[{'Name': user['Name'], 'Age': user['Age']} for user in users]
    return flask.jsonify(output)

@app.route("/delete_many/<name>")
def delete_many(name):
   if(name.isnumeric()):
      filt={'Age': name}
   else:
      filt={'Name': name}
   db.users.delete_many(filt)
   output=db.users.find()
   return flask.jsonify([{ 'Name' : op['Name'], 'Age' : op['Age'] } for op in output])

@app.route("/delete_one/<name>")
def delete_one(name):
   if(name.isnumeric()):
      filt={'Age': name}
   else:
      filt={'Name': name}
   db.users.delete_one(filt)
   output=db.users.find()
   return flask.jsonify([{ 'Name' : op['Name'], 'Age' : op['Age'] } for op in output])


@app.route("/home")
def home():
   return render_template('basic.html', db = db.users)

@app.route("/menu", methods=["POST"])
def menu():
   name=request.form.get("n")
   email=request.form.get("e")
   passwd=request.form.get("p")
   return "<h1> Welcome "+name+" </h1>"


app.run(port=5555, debug=True)