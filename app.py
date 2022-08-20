
from flask import Flask , jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alldata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class users(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200), nullable= False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods = ["GET","POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        # todo = users(title = "first todo", desc = "this is my first todo data")
        todo = users(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = users.query.all()
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = users.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods = ["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = users.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = users.query.filter_by(sno=sno).first()
    return render_template("update.html",todo = todo)





@app.route("/about")
def about():
    return "<h1>this is about page </h1>"


@app.route("/json")
def json():
    data = {
        "fname" : "Atul Kumar ",
        "lname" : "Pandey",
        "age" : 23,
        "gender": "Male",
        "role" : "DevOps engineer"
    }
    return jsonify(data)

    

if __name__ == "__main__":
    app.run(debug=True, port=5000)