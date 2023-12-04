from flask import Flask, render_template
from flask import request, redirect, url_for
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
try :
    db = pymysql.connect(
        host = 'crudkel5.mysql.database.azure.com',
        user = 'crudkel5',
        password = 'kelompok5@_#',
        db = 'crudkel5',
        ssl = {'ca' :os.getenv("SSL")}
    )
    print('berhasil konek ke database')
    print(os.getenv('DB_NAME'))
except Exception as err:
    print(f'gagal konek ke database, error: {err}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')
    
#menambah data baru
@app.route('/add/')
def add():
    return render_template('add.html')

#proses menambah data baru
@app.route('/proses_add/', methods=['POST'])
def proses_add():
    nim = request.form['nim']
    nama = request.form['nama']
    kelas = request.form['kelas']
    prodi = request.form['prodi']
    cur = db.cursor()
    cur.execute('INSERT INTO datakel5 (nim, nama, kelas, prodi) VALUES (%s, %s, %s, %s)', (nim, nama, kelas, prodi))
    db.commit()
    return redirect(url_for('add'))

#menghapus data
@app.route('/delete/')
def delete():
    return render_template('delete.html')

#proses menghapus data
@app.route('/proses_delete/', methods=['POST'])
def proses_delete():
    nim = request.form['nim']
    cur = db.cursor()
    cur.execute('DELETE FROM datakel5 WHERE nim=%s', (nim,))
    db.commit()
    return redirect(url_for('delete'))

#update data
@app.route('/update/')
def update():
    return render_template('update.html')

#proses update data
@app.route('/proses_update/', methods=['POST'])
def proses_update():
    nim = request.form['nim']
    new_nim = request.form['new_nim']
    new_name = request.form['new_name']
    new_kelas = request.form['new_kelas']
    new_prodi = request.form['new_prodi']

    cur = db.cursor()
    cur.execute('UPDATE datakel5 SET nim=%s, nama=%s, kelas=%s, prodi=%s WHERE nim=%s', (new_nim, new_name, new_kelas, new_prodi, nim))
    db.commit()
    
    return redirect(url_for('update'))


#result data
@app.route('/result/')
def result():
    cursor = db.cursor()
    cursor.execute('select * from datakel5')
    res = cursor.fetchall()
    cursor.close()
    return render_template('result.html',hasil = res)

if __name__ == '__main__':
    app.run(debug=True)

