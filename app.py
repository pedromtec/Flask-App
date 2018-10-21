from flask import Flask, render_template, request, flash, session, redirect, url_for, logging
from data import dados
from forms import RegisterForm, EditorialForm
from passlib.hash import sha256_crypt
from db import Db
from functools import wraps

db = Db('base.db')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles = dados)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

#user register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        db.save("INSERT INTO users(name, email, username, password) VALUES('{}', '{}','{}', '{}')".format(name, email, username, password))
        flash('Boa, agora você pode logar no IFCE-CP', 'success')
        return render_template('login.html')

    return render_template('register.html', form=form)

#user login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        print(username)
        data = db.find_one("SELECT * FROM users WHERE username = '{}'".format(username))
        print(data)
        if data != None:
            password = data[4]
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('Boa garoto, agora você está logado', 'success')
                return redirect(url_for('dashboard'))
            else:
                print("No matched")
                error = 'Login invalido!'
                return render_template('login.html', error=error)
        else:
            error = 'username não encontrado!'
            return render_template('login.html', error=error)

    return render_template('login.html')



def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Não autorizado, faça o login', 'danger')
            return redirect(url_for('login'))
    return wrap

#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

#logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Você saiu!", 'sucess')
    return redirect(url_for('login'))

#Add editorial
@app.route('/add_editorial', methods = ['POST', 'GET'])
@is_logged_in
def add_editorial():

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
    

