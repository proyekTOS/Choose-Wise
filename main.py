from flask import Flask, render_template, request, redirect, url_for, session
import random
import time
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def login():
 
 con = sql.connect("quotes.db")
 cur = con.cursor()
 cur.execute("SELECT * FROM quotes order by random() limit 1")
 quote = cur.fetchone()
 con.close()
 return render_template('login.html',quote=quote)

@app.route('/index')
def index():
 con = sql.connect("polling.db")
 con.row_factory = sql.Row
 cur = con.cursor()
 
 cur.execute("SELECT * FROM QUESTION order by random() limit 1")
 question = cur.fetchone()
 return render_template('index.html',question=question,id = id)

@app.route('/answer/<idQuestion>', methods = ['POST'])
def choose_answer(idQuestion):
 con = sql.connect('polling.db')
 cur = con.cursor()
 if request.form.get('first',None)!=None:
 	cur.execute("UPDATE question set choice1=choice1+1 where id = ?",[idQuestion])
	#cur.execute("INSERT INTO question
 else:
 	cur.execute("UPDATE question set choice2=choice2+1 where id = ?",[idQuestion])
 con.commit()
 con.close()
 return redirect(url_for('view_result',idQuestion=idQuestion))

@app.route('/index/result/<idQuestion>')
def view_result(idQuestion):
 con = sql.connect('polling.db')
 cur = con.cursor()
 con.row_factory = sql.Row
 cur.execute("SELECT choice1 from question where id = ?",[idQuestion])
 total_green = cur.fetchone()[0]
 cur.execute("SELECT choice2 from question where id = ?",[idQuestion])
 total_red = cur.fetchone()[0]
 cur.execute("SELECT * FROM question WHERE id = ?",[idQuestion])
 question = cur.fetchone()
 con.close()
 return render_template("result.html",green_chooser = total_green, red_chooser = total_red, question = question )
 
@app.route('/edit_profile_pic/<id>', methods = ['POST'])
def edit_profile_pic(id):
 con = sql.connect('polling.db')
 cur = con.cursor()
 imgurl = request.form['imageurl']
 cur.execute("UPDATE users set image_url = ? where id = ?",[imgurl,id])
 con.commit()
 con.close()
 return redirect(url_for('profile',id=id))

@app.route('/Creator')
def create_question():
 return render_template('Creator.html')
 
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
  cur.execute("select COUNT(*) from users where username = ? and password = ?",[username,password])
  count = cur.fetchone()[0]
  if count > 0 :
	  cur.execute("select * from users where username = ? and password = ?",[username,password])
	  row = cur.fetchone()
	  session['id'] = row[0]
	  session['username'] = row[1]
	  con.close()
	  return redirect(url_for("index"))
  else:
	  con.close()
	  con = sql.connect("quotes.db")
	  cur = con.cursor()
	  cur.execute("SELECT * FROM quotes order by random() limit 1")
	  quote = cur.fetchone()
	  return render_template("login.html",type="login",quote=quote)
  
 if request.form.get('register',None) != None:
  email=request.form['email']
  cur.execute("select COUNT(*) as hitung from users")
  row = cur.fetchone()
  cur.execute("insert into users (email, username, password) values (?,?,?)",(email,username,password))
  con.commit()
	
  con.close()
  con = sql.connect("quotes.db")
  cur = con.cursor()
  cur.execute("SELECT * FROM quotes order by random() limit 1")
  quote = cur.fetchone()
  return render_template('login.html',type="register",quote=quote)

@app.route('/ins_quest/<id_user>', methods = ['POST'])
def input_quest(id_user):
  con = sql.connect("polling.db")
 
  cur = con.cursor()
  if request.form.get('Creator',None) != None:

		quest=request.form['quest']

		first_choice=request.form['pil1']

		second_choice=request.form['pil2']
		
		cur.execute("insert into question (question, first_choice, second_choice, choice1, choice2, user_id) values (?,?,?,?,?,?)",[quest,first_choice,second_choice,0,0,id_user])
		con.commit()
		con.close()
		return redirect(url_for("index",id_user=id_user))

@app.route('/del_quest/<id>',methods=['GET', 'POST'])
def delete_question(id):
 con = sql.connect("polling.db")
 con.row_factory = sql.Row
 cur = con.cursor()
 msg = "msk"	
 cur.execute("delete from question where id=?",[id])
 con.commit()
 con.close()
 return redirect(url_for('profile',id=session['id']))

@app.route('/logout')
def logout():
  session.pop('id',None)
  session.pop('username',None)
  return redirect(url_for('login'))

@app.route('/profile/<id>')
def profile(id):
  con = sql.connect('polling.db')
  cur = con.cursor()
  con.row_factory = sql.Row
  cur.execute("SELECT * FROM users WHERE id = ?",[id])
  profile = cur.fetchone()
  cur.execute("SELECT * from question where user_id = ?",[id])
  questions = cur.fetchall()
  con.close()
  return render_template('profile.html',profile = profile, questions = questions)

if __name__ == '__main__':
 app.debug = True
 app.run('0.0.0.0',15043)
