import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#create app
app=Flask(__name__)

#config environment with keywords as dictionary
app.config.from_object(__name__)
app.config.update(dict(
	DATABASE=os.path.join(app.root_path,"miniblog.db"),
	DEBUG=True,
	SECRET_KEY="deve", #as complex as possible os.urandom(24)	
	USERNAME='K', #login username
	PASSWORD='1', #login password
)
)

#set up the link to database
def connect_db():
	rv=sqlite3.connect(app.config['DATABASE']) #connect to miniblog.db
	rv.row_factory=sqlite3.Row
	return rv #return an object containing all rows in db

#get the access to and/or create miniblog.db if not exist
def get_db():
	if not hasattr(g, "sqlite_db"):
		g.sqlite_db=connect_db() 
	return g.sqlite_db

#initialize db
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')

#close db connect if any error or tranction is done well 
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()



#****** homepage ******  (nothing but redirect)
@app.route('/')
def index ():
	return redirect(url_for('login'))


#****** login page ****** (view + processing)
@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username']!=app.config['USERNAME'] or request.form['password']!=app.config['PASSWORD']:
			error='invalid password or username'
		else:
			session['logged_in']=True  #use logged_in label to indicate login status
			flash('You were logged in')
			return redirect(url_for('user'))
	return render_template('login.html', error=error) # return to login page 


#****** list posting ******	(view)	
@app.route('/user', methods=['POST','GET'])
def user():
	db=get_db()
	cur=db.execute('select title,content from entries order by id desc')
	entries=cur.fetchall()	
	return render_template('user.html', entries=entries)

#****** add posting to table of db ******  (processing)
@app.route('/add', methods=['GET','POST'])
def add():
	if not session.get('logged_in'):
		abort(401)
	db=get_db()
	db.execute('insert into entries (title, content) values (?, ?)', [request.form ['title'], request.form['content']])
	db.commit()
	flash('New entry was added')
	return redirect(url_for('user'))	
	
#****** logout and return to login page ******  (view and processing)
@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('you were logged out')
	return redirect(url_for('login'))

# run by installing
'''
if __name__=='__main__':
	app.run(debug=True)
'''





