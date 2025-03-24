from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import String

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    SLno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SLno} - {self.Title}"

@app.route("/",methods=['GET','POST'])
def input():
    allTodo = Todo.query.all()
    if request.method=='POST':
        Title=request.form['Title']
        Desc=request.form['Desc']
        M = Todo(Title=Title, Desc=Desc)
        db.session.add(M)
        db.session.commit()
    return render_template('index.html',allTodo=allTodo)


@app.route('/delete<int:SLno>')
def delete(SLno):
    alltodo=Todo.query.filter_by(SLno=SLno).first()
    db.session.delete(alltodo)
    db.session.commit()

    return redirect("/")

@app.route('/update<int:SLno>',methods=['GET','POST'])
def update(SLno):
    todo = Todo.query.filter_by(SLno=SLno).first()
    if request.method=='POST':
        todo.Title=request.form['Title']
        todo.Desc=request.form['Desc']
        
        db.session.commit()
    return render_template('update.html',todo=todo)




if __name__ == "__main__":
    app.run(port=5001, debug=True)