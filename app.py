from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'oculto'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO usuarios VALUES (1, 'admin', 'admin')")
    conn.commit()
    conn.close()
init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
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
    if request.method == 'POST':
        edad = request.form['edad']
        sexo = request.form['sexo']
        presion = request.form['presion']
        colesterol = request.form['colesterol']
        # aplicar machine learning 
        resultado = "Riesgo bajo" if int(colesterol) < 200 else "Riesgo alto"
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