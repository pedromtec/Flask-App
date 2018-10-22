from flask import Flask, render_template, request, flash, session, redirect, url_for, logging
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


@app.route('/editorials')
def editorials():
    editorials = db.find_all('SELECT * FROM editorials')
    if len(editorials) > 0:
        return render_template('editorials.html', editorials=editorials)
    else:
        return render_template('editorials.html')
    

@app.route('/editorial/<string:id>/')
def editorial(id):
    editorial = db.find_one("SELECT * FROM editorials WHERE id = '{}'".format(id))
    return render_template('editorial.html', editorial=editorial)

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
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#user login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        data = db.find_one("SELECT * FROM users WHERE username = '{}'".format(username))
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
    editorials = db.find_all("SELECT * FROM editorials where author = '{}'".format(session['username']))
    if len(editorials) > 0:
         return render_template('dashboard.html', editorials=editorials)
    else:
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
    form = EditorialForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        db.save("INSERT INTO editorials(title, body, author) VALUES('{}', '{}','{}')".format(title, body, session['username']))
        flash('Editorial salvo com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_editorial.html', form = form)

#Edit editorial
@app.route('/edit_editorial/<string:id>', methods = ['POST', 'GET'])
@is_logged_in
def edit_editorial(id):
    form = EditorialForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        db.update("UPDATE editorials SET title='{}', body='{}' WHERE id = '{}'".format(title, body, id))
        flash('Editorial editado', 'sucess')
        return redirect(url_for('dashboard'))

    editorial = db.find_one("SELECT * FROM editorials WHERE id = '{}'".format(id))
    form.title.data = editorial[1]
    form.body.data = editorial[3]

    return render_template('edit_editorial.html', form = form)

@app.route('/delete_editorial/<string:id>', methods = ['POST'])
@is_logged_in
def delete_editorial(id):
    db.delete("DELETE FROM editorials WHERE id = '{}'".format(id))
    flash('Editorial apagado', 'sucess')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
    

