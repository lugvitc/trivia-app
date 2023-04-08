from flask import Flask, request, Response, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

api = Flask(__name__)
CORS(api)

api.secret_key = "mySecretKey"
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivia.db'

db = SQLAlchemy(api)

# define database models:
class Trivia(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(128), nullable=False, unique=False)
    option1 = db.Column(db.String(128), nullable=False, unique=False)
    option2 = db.Column(db.String(128), nullable=False, unique=False)
    option3 = db.Column(db.String(128), nullable=False, unique=False)
    option4 = db.Column(db.String(128), nullable=False, unique=False)
    correctAnswer = db.Column(db.String(128), nullable=False, unique=False)

@api.route('/')
def welcome():
    return "Hi, welcome to the backend of Trivia APP!"

@api.route('/create-db')
def createDB():
    try:
        db.create_all()
        return "Hey, Trivia DB creation was successful!"
    except:
        return "Sorry, there was an error while creating the database"

@api.route('/add-questions', methods=['GET','POST'])
def addQuestions():
    if request.method=="GET":
        return render_template("add_questions.html")
    elif request.method=="POST":
        try:
            unique_id = int(request.form['unique_id'])
            question = request.form['question']
            option1 = request.form['option1']
            option2 = request.form['option2']
            option3 = request.form['option3']
            option4 = request.form['option4']
            correctAnswer = request.form['correctAnswer']
            print(unique_id, question, option1, option2, option3, option4, correctAnswer)
            record = Trivia(unique_id=unique_id, question=question, option1=option1, option2=option2, option3=option3, option4=option4, correctAnswer=correctAnswer)
            db.session.add(record)
            db.session.commit()
            return "Hey, the record with id " + str(unique_id) + " was successfully added!"
        except Exception as e:
            print(e)
            return "Sorry, could not add your question with id! " + str(request.form['unique_id'])

if "__name__"=="__main__":
    api.run(debug=True)