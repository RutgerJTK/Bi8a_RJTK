import os

import pymysql
from flask import Flask, render_template, request

martin_folder = os.path.join('static', 'MartinCat.jpeg')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():  # put application's code here
    return render_template('homepage.html')


@app.route('/week_1', methods=['GET', 'POST'])
def week_1():  # enter week 1 homepage
    try:
        str_results = ""
        str_list = []
        if request.method == 'POST':
            query = request.form['query_1']
            print("*" * 80)
            db = pymysql.connect(host="ensembldb.ensembl.org",
                                 user="anonymous",
                                 password="",
                                 database="homo_sapiens_core_95_38")
            cursor = db.cursor()
            cursor.execute("SHOW Tables")
            cursor.execute("""SELECT * FROM gene where description like %(p)s limit 10""",
                           {"p": "%{}%".format(query)})
            results = cursor.fetchall()
            cursor.close()
            db.close()
            print(len(query), "and: ", len(results))

            if len(query) and len(results) >= 1:
                print(len(query), "and: ", len(results))
                for i in results:
                    str_results = (i[8] + ": " + i[9])
                    str_list.append(str_results)
                return render_template('week1.html', myresults=str_list, query=query)
            else:
                return render_template('week1.html',
                                       noresults="No results were found - please search again \
                                       you poor excuse for a human being ^-^")
        else:
            print("")
        return render_template('week1.html')
    except IOError:
        print("Something went wrong")
    except Exception as E:
        print("Something went wrong::", "\n", E)


@app.route('/week_2', methods=['GET', 'POST'])
def week_2():  # enter week 1 homepage
    try:
        if request.method == 'post':
            print("Entered week 2!")
            return render_template('week2.html')
        return render_template('week2.html')
    except Exception as E:
        print(E)


if __name__ == '__main__':
    app.add_url_rule('/', 'homepage', homepage)
    app.run(host="localhost", port=5000)
