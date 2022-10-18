import os

import pymysql
from flask import Flask, render_template, request
from Bio import Entrez
from pymysql import Connect
# from mysql import mysql.connector
martin_folder = os.path.join('static', 'MartinCat.jpeg')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():  # put application's code here

    return render_template('homepage.html')


@app.route('/week_1', methods=['GET', 'POST'])
def week_1():   # enter week 1 homepage
    print("yoyo")
    if request.method == 'POST':
        query = request.form['query_1']
        print(query)
        print("*"*80)
        # Entrez.email = 'rjtkemperman@gmail.com'
        # data = Entrez.esearch(db="", term=query)
        # record = Entrez.read(data)
        # print(record)
        db = pymysql.connect(host="ensembldb.ensembl.org",
            user="anonymous",
            password="",
            database="homo_sapiens_core_95_38")
        cursor = db.cursor()
        cursor.execute("SHOW Tables")
        cursor.execute('''SELECT * FROM gene where description like {'havana%'} limit 10''')
        print(cursor.description)
        myresults = cursor.fetchall()
        for x in myresults:
            print(*x)
        cursor.close()
        db.close()

    else:
        print("")
    return render_template('week1.html')


@app.route('/week_2', methods=['GET', 'POST'])
def week_2():   # enter week 1 homepage
    try:
        if request.method == 'post':
            print("Wow!")

            return render_template('week2.html')
        return render_template('week2.html')
    except Exception as E:
        print(E)


if __name__ == '__main__':
    app.add_url_rule('/', 'homepage', homepage)
    app.run(host="localhost", port=5000)
