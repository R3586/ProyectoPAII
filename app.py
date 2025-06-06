from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'oculto'


@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas', 'error')
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/diagnostico', methods=['GET', 'POST'])
def diagnostico():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    resultado = None

    return render_template('diagnostico.html', resultado=resultado)

@app.route('/noticias')
def noticias():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('noticias.html')

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # por si hat tiempo se agregan mas funciones
    return render_template('configuracion.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    if not os.path.exists(app.config ['UPLOAD_FOLDER']):
        os.makedirs(app.config [ 'UPLOAD_FOLDER'])
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))

#if __name__ == '__main__':
#    app.run(debug=True)
