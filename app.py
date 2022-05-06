# app.py
import uuid

from decomposition_final import *
from image_to_text import *
from flask_mysqldb import MySQL
from flask import Flask, render_template, flash, redirect, url_for, request,jsonify

from werkzeug.utils import secure_filename
from flask_cors import CORS

import os

from psycopg2 import DatabaseError, InterfaceError, connect
import psycopg2


# ---------------------------------------------- main
# identifiants de la connexion
"""
USER = "admpersonnes"
PASSWD = "password"
HOST = "localhost"
DATABASE = "flask"
"""

# connexion d'un utilisateur existant



# Open a cursor to perform database operations



# configuration avec base de donnée flask

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'pcd'
app.config['MYSQL_PORT'] =3306


mysql = MySQL(app)


UPLOAD_FOLDER = 'static/img'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
id=1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""
conn = mysql.connect(
        host="localhost",
        database="flask",
        user="root",
        password="123456789")"""
@app.route('/')
def index():
    print(5)

    cur = mysql.connection.cursor()
    #DROP TABLE IF EXISTS `cheque`;
    cur.execute('''
DROP TABLE IF EXISTS cheque1;

CREATE TABLE cheque1 (
    
	id SERIAL PRIMARY KEY,
	nomtitulaire VARCHAR(255) NOT NULL,
	rib VARCHAR(255) NOT NULL,
	numcheque VARCHAR (255),
	agence VARCHAR (255),
	description VARCHAR (255),
        last_update DATE
);


''')
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])

def upload():
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    inputEmail = request.form['inputEmail']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        decomposition_le_cheque_en_image(filename)
        list =rib('titulaire.png')
        if list == -1 :
            nomtitulaire = '-1'
            rib_titulaire = '-1'
        else :
            nomtitulaire = list[4]
            rib_titulaire = list[0]+list[1]+list[2]+list[3]

        numcheque = numero_cheque('numcheque.png')
        agence = adresse_bank('payable.png')

        cur = mysql.connection.cursor()
        cur.execute('''
               INSERT INTO cheque1(nomtitulaire,rib,numcheque,agence) VALUES( %s,%s,%s,%s) ;''',(nomtitulaire,rib_titulaire,numcheque,agence))
        mysql.connection.commit()
        cur.close()
        return redirect('/good-job')
    else:
        return redirect('/terminaison/invalid')

@app.route('/api/addpost',methods=['POST'])
def addpost():
    return  jsonify(data= "the post was created successfully")
    if request.method =='POST':
        print(request.form,flush=True)

        titre = request.form.get("titre")
        content = request.form.get("content")
        cover =request.files["cover"]
        if cover and allowed_file(cover.filename):
            filename = str(uuid.uuid4())
            filename += "."
            filename += cover.filename.split(".")[1]
            #create secure name
            filename_secure =secure_filename(filename)
            #save the file inside the uploads folder
            cover.save(os.path.join(app.config["UPLOAD_FOLDER"],filename_secure))
            #local file
            local_file ="./uploads"

if __name__ == '__main__':
    app.run(debug=True)
