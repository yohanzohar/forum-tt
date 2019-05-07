# from flask import render_template, request, redirect, url_for, flash, session
# from base import app, db, User, Discussion, Message
# from utils import validate_password

# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route('/')
# def index():
#   discussions = Discussion.query.all()
#   return render_template('index.html', discussions=discussions)

# @app.route('/messages/<int:discussion_id>', methods=['POST', 'GET'])
# def discussion(discussion_id):
#   if request.method == 'POST':
#     user = User.query.filter_by(username=session['username']).first()
#     message = Message(
#       text=request.form['text'],
#       discussion_id=discussion_id,
#       user_id=user.id
#     )
#     db.session.add(message)
#     db.session.commit()

#   discussion = Discussion.query.filter_by(id=discussion_id).first()
#   messages = Message.query.filter_by(discussion_id=discussion_id).all()
  
#   for message in messages:
#     message.user = User.query.filter_by(id=message.user_id).first()

#   return render_template('messages.html', messages=messages, discussion=discussion)

# # @app.route('/signup', methods=['GET', 'POST'])
# # def signup():
# #   if 'username' in session:
# #     return redirect( url_for('index') )

# #   if request.method == 'POST':
# #     user = User(
# #       username=request.form['username'],
# #       password=request.form['password']
# #     )

# #     db.session.add(user)
# #     db.session.commit()
    
# #     return redirect( url_for('index') )

# #   return render_template('signup.html')
# @app.route('/signup',methods = ['GET', 'POST'])
# def signup():
#     if 'username' in session:
#         return redirect(url_for('index'))
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if User.query.filter_by(username=username).first() == None:
#             if password_check(password):
#                 user = User(username=username,password=password)
#                 flash('User saved succefuly')
#                 db.session.add(user)
#                 db.session.commit()
#                 session['username'] = username
#                 return redirect(url_for('index'))
#             else:
#                 flash(' password is too weak')
#         else:
#             flash('Username already exist')
#     return render_template('signup.html')




# @app.route('/login/', methods=['POST', 'GET'])
# def login():
#   if 'username' in session:
#     return redirect( url_for('index') )

#   if request.method == 'POST':
#     user = User.query.filter_by(
#       username=request.form['username'],
#       password=request.form['password']
#     ).first()

#     if user:
#       session['username'] = request.form['username']
#       return redirect( url_for('index') )

#     flash('Invalid credentials')

#   return render_template('login.html')


# @app.route('/logout/')
# def logout():
#   if 'username' in session:
#     session.pop('username')

#   return redirect( url_for('index') )

# @app.route('/profil/<int:user_id>', methods=['GET', 'POST'])
# def profile(user_id):
# 	user = User.query.filter_by(id=user_id).first()
# 	messages = Message.query.filter_by(user_id=user_id).all()
# 	if request.method == 'POST':
# 		if 'new_username' in request.form:
# 			new_username= request.form['new_username']
# 			searched_user = User.query.filter_by(username=new_username).first()
# 			if searched_user == None:
# 				user.username = new_username
# 				db.session.commit()
# 				session['username'] = new_username
# 				return redirect(request.path, code=302)
# 			else:
# 				flash('username is a already taken')			
# 		elif 'old_password' in request.form:
# 			old_password = request.form['old_password']
# 			new_password = request.form['new_password']
# 			user = User.query.filter_by(
# 		      username=session['username'],
# 		      password=old_password
# 		    ).first()
# 			if user != None:
# 				if validate_password(new_password) and new_password != old_password:
# 					user.password = new_password
# 					flash('you change your password')
# 					db.session.commit()		
# 				else:
# 					flash('new password is too weak')
# 			else:
# 				flash('Invalid password')

# 	return render_template('profile.html',user=user,messages=messages)
from flask import session, render_template, request, redirect, url_for,flash
from base import app, db, User, Discussion, Message
from sqlalchemy import desc
from utils import validate_password

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

@app.route('/')
def index():
    discussions = Discussion.query.all()
    messages = Message.query.all() 
    user = User.query.all()
    messages_number = len(messages)
    dernier_message = messages[-1]
    return render_template('index.html', discussions=discussions,messages=messages,user=user,messages_number=messages_number,dernier_message=dernier_message)

@app.route('/messages/<int:discussion_id>', methods=['POST', 'GET'])
def discussion(discussion_id):
  if request.method == 'POST':
    user = User.query.filter_by(username=session['username']).first()
    message = Message(
      text=request.form['text'],
      discussion_id=discussion_id,
      user_id=user.id
    )
    db.session.add(message)
    db.session.commit()

  discussion = Discussion.query.filter_by(id=discussion_id).first()
  messages = Message.query.filter_by(discussion_id=discussion_id).all()
  
  for message in messages:
    message.user = User.query.filter_by(id=message.user_id).first()

  return render_template('messages.html', messages=messages, discussion=discussion)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first() == None:
            if validate_password(password):
                user = User(username=username,password=password)
                db.session.add(user)
                db.session.commit()
                session['username'] = username # pour qu'il se connect directe
                return redirect(url_for('index'))
            else:
                flash('Password is too weak!!')
        else:
            flash('Username is already taken')
    return render_template('signup.html')


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if 'chances' not in session:
        session['chances'] = 3 
    print(session['chances'])
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if session['chances'] <= 1:
            flash('Too many login attempts')
        else:
            user = User.query.filter_by(
                username=request.form['username'],
                password=request.form['password']
            ).first()
            if user:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                session['chances'] -= 1 
                flash('Invalid credentials you have {} chances remaining'.format(session['chances']))
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route('/profil/<int:user_id>')
def profile(user_id):
	user = User.query.filter_by(id=user_id).first()
	messages = Message.query.filter_by(user_id=user_id).all()
	return render_template('profile.html',user=user,messages=messages)

@app.route('/profil/<int:user_id>/password', methods=['POST'])
def password_update(user_id):
  if 'old-password' in request.form:
    old_password = request.form['old-password']
    new_password = request.form['new-password']
    user = User.query.filter_by(
      username=session['username'],
      password=old_password
    ).first()

    if user != None:
      user.password = new_password
      db.session.commit()
    else:
      flash('Invalid password')

  return redirect( url_for('profile', user_id=user_id) )


@app.route('/profil/<int:user_id>/username', methods=['POST'])
def username_update(user_id):
  user = User.query.filter_by(id=user_id).first()
  if 'new-username' in request.form:
    new_username = request.form['new-username']
    searched_user = User.query.filter_by(username=new_username).first()
    if searched_user == None:
      user.username = new_username
      db.session.commit()
      session['username'] = new_username
    else:
      flash('Username is already taken')

  return redirect( url_for('profile', user_id=user.id) )`




#git = service de versioning 