
from flask import Flask, render_template, request, redirect  # any page show 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Standup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Standup(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    update =  db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:                    #what to print
        return f"{self.SrNo} - {self.Name}"

@app.route('/', methods=['GET','POST'])
def hello_world(): 
    if request.method=='POST':
        Name = request.form['Name']
        update = request.form['update']
        daily = Standup(Name=Name, update=update)
        db.session.add(daily)
        db.session.commit()
        
    allStandup = Standup.query.all()
    return render_template('index.html', allStandup=allStandup)

@app.route('/show')
def products():
    allStandup = Standup.query.all()
    print(allStandup)
    return "this is product page"

@app.route('/Edit/<int:SrNo>', methods=['GET','POST'])
def Edit(SrNo):
    if request.method=='POST':
        Name = request.form['Name']
        update = request.form['update']
        daily = Standup.query.filter_by(SrNo=SrNo).first()
        daily.Name = Name
        daily.update = update
        db.session.add(daily)
        db.session.commit()
        return redirect("/")
        
    daily = Standup.query.filter_by(SrNo=SrNo).first()
    return render_template('Edit.html', daily=daily)

@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    daily = Standup.query.filter_by(SrNo=SrNo).first()
    db.session.delete(daily)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000) #make it false at end

