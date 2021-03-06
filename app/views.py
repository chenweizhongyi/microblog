from app import app,db, lm, oid
from flask import render_template,flash,redirect, session, url_for, request, g
from .forms import LoginForm,SigninForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

#登录视图函数
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if User().Account_Judgment(form.username.data,form.password.data):
            session['username'] = form.username.data
            login_user(User())
            return redirect(url_for('user',username=form.username.data))
        else:
            flash('用户名或密码错误')
    # if form.validate_on_submit():
    #     session['remember_me'] = form.remember_me.data
    #     return oid.try_login(form.openid.data,ask_for=['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#flask——openid 登录回调
@oid.after_login
def after_login(resp):
    if resp.email is None and resp.email == '':
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
# @login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('user' + username + 'not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
        user = user,
        posts = posts)

@app.route('/signin',methods=['POST','GET'])
def signin():
    form = SigninForm()
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            flash('两次输入的密码不一致')
        if User().valid_regist(form.username.data,form.email.data):
            user = User(username=request.form['username'], password=request.form['password1'],
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash('注册成功')
        else:
            flash('用户名或邮箱已经存在')
    return render_template(
        'signin.html',
        form = form
    )