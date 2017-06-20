from flask import Flask, render_template, request, redirect, url_for
import time
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def login():
 return render_template('login.html')

@app.route('/index')
def index():
 return render_template('index.html')

@app.route('/create_question')
def create_question():
 con = sql.connect("polling.db")
 con.row_factory = sql.Row
 cur = con.cursor()
 cur.execute("SELECT * from question")
 rows = cur.fetchall()
 return render_template('creator.html', rows = rows)
 
@app.route('/register')
def register():
 return render_template('register.html')
 
@app.route('/login', methods = ['POST'])
def check():

 con = sql.connect("polling.db")
 
 cur = con.cursor()
 
 
 if request.form.get('username',None) != None:
  username=request.form['username']
 
 if request.form.get('password',None) != None:
  password=request.form['password']
 
 if request.form.get('login',None) != None:
  cur.execute("select COUNT(*) as hitung from user where username = ? and password = ?",[username,password])
  count = cur.fetchone()
  if(count[0]==1):
   return redirect(url_for("index"))
  else:
   return redirect(url_for("login"))

 if request.form.get('Creator',None) != None:
  if request.form.get('quest',None) != None:
    quest=request.form['quest']
  if request.form.get('pil1',None) != None:
    first_choice=request.form['pil1']
  if request.form.get('pil2',None) != None:
    second_choice=request.form['pil2']
  cur.execute("select MAX(ID) as hitung from question")
  row = cur.fetchone()
  if row[0] == None:
      max = 1
  else:
      max = row[0]+1
  try:
   cur.execute("insert into question (id, question, first_choice, second_choice) values (?,?,?,?)",(max,quest,first_choice,second_choice))
   con.commit()
   msg = "Record successfully added"
  except:
   con.rollback()
   msg = "error in insert operation"
  con.close()
  return redirect(url_for("create_question",msg = msg))
   
 if request.form.get('register',None) != None:
  email=request.form['email']
  cur.execute("select MAX(ID) as hitung from user")
  row = cur.fetchone()
  if row[0] == None:
      max = 1
  else:
      max = row[0]+1
  try:
   cur.execute("insert into user (id, email, username, password) values (?,?,?,?)",(max,email,username,password))
   con.commit()
   msg = "Record successfully added"
  except:
   con.rollback()
   msg = "error in insert operation"
  con.close()
  return redirect(url_for("login",msg = msg))
  
if __name__ == '__main__':
 app.debug = True
 app.run('0.0.0.0',5056)
